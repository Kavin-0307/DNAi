def docstring():
    """ the main thing i understood is that this engine basically kinda sets a threshold of what to include as the final output and what not to.
    it sorts all the results too
    """
def ranking_engine(final_scores:dict,top_n:int =4)->dict:
    default_threshold=0.5
    ranked_results=dict(sorted(final_scores.items(),key=lambda item:item[1],reverse=True))
    filtered={}
    for disease,score in ranked_results.items():
        if score<0.5:
            continue
        else:
            filtered[disease]=score
    top_results=dict(list(filtered.items())[:top_n])
    return top_results
        
    