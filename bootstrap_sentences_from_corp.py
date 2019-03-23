def bootstrap(target_word, keys, corp_text, l_window=15, r_window=15, extra_width=0):
    """
    target_word: str
    keys: str, or a list of str
    corp_text: A long str
    l_window, r_window: window size set to look for sentences matching `keys` in `corp_text`
    extra_width: Additional width added to `l_window` & `r_window` to the returned extracted sentences
    """
    
    # Find windows containinig target word
    match_target_idx = find_all_target_word_window(target_word, corp_text, l_window, r_window)
    
    # bootstrapped sentences from `target_word` and `keys` from `corp_text`
    extracted_sentences = filter_by_seed(keys, match_target_idx, corp_text, extra_width)
    return(extracted_sentences)


def find_all_target_word_window(target, text, l_window=15, r_window=15):
    start = 0
    match_idx = []
    text_len = len(text)
    while True:
        start = text.find(target, start)
        if start != -1:
            
            # Get a window range containing target word
            left_idx = 0 if (start - l_window) < 0 else (start - l_window)
            right_idx = text_len if (start + len(target) + r_window > text_len) else (start + len(target) + r_window)
            match_idx.append([left_idx, right_idx])
            
            start = right_idx + 1 if (right_idx < text_len) else text_len
        else:
            return(match_idx)
    return(match_idx)


def filter_by_seed(seed_sent_keys, candidate_sent_idx, corp_text, extra_width=0):
    """
    seed_sent_keys: str or a list of words obtained from the seed sentence
    candidate_sent_idx: Two-level nested list: [[l_idx, r_idx], [l_idx, r_idx], ..., [l_idx, r_idx]]
    corp_text: str
    """
    extr_sent = []
    
    # Loop over every candidate sentences in `corp text` that contains the target word 
    # as specified in `find_all_target_word_window()`
    #
    # if all words in `seed_sent_keys` are present in the candiate sentence, 
    # then extract that sentence
    for rng in candidate_sent_idx:
        candidate_sentence = corp_text[rng[0]:rng[1]]
        
        # Check whether all word in seed_sent_keys are present in candidate_sentence
        valid = True
        for keyword in seed_sent_keys:
            if candidate_sentence.find(keyword) == -1: 
                valid = False
                break
        
        if valid == True:
            # Append the candidate sentence to the list to be output
            left_idx = 0 if (rng[0] - extra_width < 0) else (rng[0] - extra_width)
            right_idx = len(corp_text) if (rng[1] + extra_width > len(corp_text)) else (rng[1] + extra_width)
            extr_sent.append(corp_text[left_idx:right_idx])
    
    return(extr_sent)
