import numpy as np
import pysubebm.utils as utils 
from typing import Tuple
import logging
 
def metropolis_hastings(
        data_matrix: np.ndarray,
        n_subtypes: int,
        diseased_arr: np.ndarray,
        iterations: int,
        n_shuffle: int,
        n_subtype_shuffle:int,
        prior_n: float,
        prior_v: float,
        rng: np.random.Generator
) -> Tuple:
    """Implement metroplis hastings MCMC algorithm
    
    """  
    n_participants, n_biomarkers = data_matrix.shape

    # Validate input
    if n_shuffle <= 1:
        raise ValueError("n_shuffle must be >= 2 or =0")
    if n_shuffle > n_biomarkers:
        raise ValueError("n_shuffle cannot exceed n_biomarkers")

    n_stages = n_biomarkers + 1
    disease_stages = np.arange(start=1, stop=n_stages, step=1)
    n_disease_stages = n_stages - 1
    non_diseased_ids = np.where(diseased_arr == 0)[0]
    diseased_ids = np.where(diseased_arr == 1)[0]

    """Initiate theta phi
        Shape: (n_subtypes, N, 4)
    """
    # N * 4 matrix, cols: theta_mean, theta_std, phi_mean, phi_std
    theta_phi_default = utils.get_initial_theta_phi_estimates(
        data_matrix, non_diseased_ids, diseased_ids, prior_n, prior_v, rng=rng)
    
    current_theta_phi = np.repeat(theta_phi_default[np.newaxis, :, :], n_subtypes, axis=0)


    """Initiate subtype ordering matrix
        Shape: (n_subtypes, n_disease_stages)
        Imagine this: the array of biomarker_int stays intact. we are randomizing the indices of each of them in the new order
    """
    current_order = np.vstack([rng.permutation(np.arange(1, n_stages)) for _ in range(n_subtypes)])

    """Initiate staging prior and post
        Stage_alpha_prior and stage_prior, shape: (n_subtypes, n_disease_stages)

        Stage posterior, shape: (n_participants, n_subtypes, n_disease_stages)
    """
    # shape: (n_subtypes, n_disease_stages)
    # dirichlet alpha prior for stage_prior
    stage_alpha_prior = np.ones((n_subtypes, n_disease_stages), dtype=np.float64)

    # index from zero here
    # Initialize stage_prior array
    # stage_prior, previoulsy I used current_pi. This is the prior distribution of N disease stages, for each subtype
    current_stage_prior = np.zeros((n_subtypes, n_disease_stages), dtype=np.float64)
    # Sample from Dirichlet distribution for each subtype, based on alpha prior
    for i in range(n_subtypes):
        current_stage_prior[i, :] = rng.dirichlet(stage_alpha_prior[i, :])
    # Only for diseased participants
    current_stage_post = np.zeros((n_participants, n_subtypes, n_disease_stages), dtype=np.float64)

    """Initiate subtype prior and subtype post
    """
    # shape: (n_subtypes, 1), dirichlet alpha prior for subtype_prior
    subtype_alpha_prior = np.ones(n_subtypes, dtype=np.float64)
    # subtype prior, sample from Dirichlet distribution, based on subtype_alpha_prior
    # shape: (n_subtypes, 1),
    current_subtype_prior = rng.dirichlet(subtype_alpha_prior)
    # shape: (n_participants, n_subtypes)
    current_subtype_post = np.zeros((n_participants, n_subtypes), dtype=np.float64)


    current_ln_likelihood = -np.inf
    acceptance_count = 0
    # Note that this records only the current accepted orders in each iteration
    all_accepted_orders = []
    # This records all log likelihoods
    log_likelihoods = []

    for iteration in range(iterations):
        random_state = rng.integers(0, 2**32 - 1)
        log_likelihoods.append(current_ln_likelihood)

        new_order = current_order.copy()
        # randomly pick n_shuffle subtype orderings to shuffle 

        shuffle_indices = rng.choice(n_subtypes, size=n_subtype_shuffle, replace=False)
        for subtype_idx in shuffle_indices:
            utils.shuffle_order(new_order[subtype_idx], n_shuffle, rng)

        """
        When we propose a new ordering, we want to calculate the total ln likelihood, which is 
        dependent on theta_phi_estimates, which are dependent on biomarker_data and stage_likelihoods_posterior,
        both of which are dependent on the ordering. 

        Therefore, we need to update participant_data, biomarker_data, stage_likelihoods_posterior
        and theta_phi_estimates before we can calculate the total ln likelihood associated with the new ordering
        """

        """
        update theta_phi_estimates
        """

        # --- Compute stage posteriors with OLD θ/φ ---
        _, stage_post_old, subtype_post_old  = utils.update_data_ln_likes_and_stage_and_subtype_post(
            data_matrix,
            non_diseased_ids,
            disease_stages,
            current_order,
            current_theta_phi,
            current_stage_prior,
            current_stage_post,
            current_subtype_prior,
            current_subtype_post
        )

        # Compute the new theta_phi_estimates based on new_order
        new_theta_phi = utils.update_theta_phi_estimates(
            n_biomarkers,
            n_participants,
            non_diseased_ids,
            data_matrix,
            new_order,
            current_theta_phi,  # Current state’s θ/φ
            stage_post_old,
            subtype_post_old,
            disease_stages,
            prior_n,    # Weak prior (not data-dependent)
            prior_v,     # Weak prior (not data-dependent)
            random_state,
        )

        # NOTE THAT WE CANNOT RECOMPUTE P(K_J) BASED ON THIS NEW THETA PHI.
        # THIS IS BECAUSE IN MCMC, WE CAN ONLY GET NEW THINGS THAT ARE SOLELY CONDITIONED ON THE NEWLY PROPOSED S'

        # Recompute new_ln_likelihood using the new theta_phi_estimates
        new_ln_likelihood, stage_post_new, subtype_post_new = utils.update_data_ln_likes_and_stage_and_subtype_post(
            data_matrix,
            non_diseased_ids,
            disease_stages,
            new_order,
            new_theta_phi,
            current_stage_prior,
            stage_post_old,
            current_subtype_prior,
            subtype_post_old,
        )
        
        # Compute acceptance probability
        delta = new_ln_likelihood - current_ln_likelihood
        prob_accept = 1.0 if delta > 0 else np.exp(delta)

        # Accept or reject the new state
        if rng.random() < prob_accept:
            current_order = new_order
            current_ln_likelihood = new_ln_likelihood
            current_stage_post = stage_post_new
            current_theta_phi = new_theta_phi
            current_subtype_post = subtype_post_new
            acceptance_count += 1

            # --- Gibbs update for π using CURRENT posteriors ---
            for i in range(n_subtypes):
                stage_counts = current_stage_post[i, diseased_ids].sum(axis=0)  # soft counts
                current_stage_prior[i] = rng.dirichlet(stage_alpha_prior[i] + stage_counts)
            
            subtype_counts = current_subtype_post.sum(axis=0) # soft counts
            current_subtype_prior = rng.dirichlet(subtype_alpha_prior + subtype_counts)


        all_accepted_orders.append(current_order.copy())

        # Log progress
        if (iteration + 1) % max(10, iterations // 10) == 0:
            acceptance_ratio = 100 * acceptance_count / (iteration + 1)
            logging.info(
                f"Iteration {iteration + 1}/{iterations}, "
                f"Acceptance Ratio: {acceptance_ratio:.2f}%, "
                f"Log Likelihood: {current_ln_likelihood:.4f}, "
            )

    return all_accepted_orders, log_likelihoods, current_theta_phi, current_stage_post, current_subtype_prior, current_stage_prior, current_subtype_post