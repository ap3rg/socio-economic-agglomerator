import pandas as pd


# Main Method
def agglomerate(df, agg_dictionary, groupby_cols):
    '''
    Main method.
    
    Method that agglomerates certain columns of a dataframe, when grouped by others
    according to by a certain scheme.
    
    This procedure first agglomerates at the same time all of the columns that take single parameter
    and then agglomerates the others one by one.
    
    Parameters
        df : Dataframe
        aggl_dictionaty : Dictionary with aggregation functions per column name
        groupby_cols : Columns to grupby
        agglomerate_cols : columns to agglomerate
        
    Returns
        Resulting DataFrame
    '''
    
    # Process functions with one argument first
    agg_dictionary_simple_func = {}
    agg_dictionary_compound_func = {}
    for key in agg_dictionary.keys():
        functions = agg_dictionary[key]
        if len(functions) == 1:
            agg_dictionary_simple_func[key] = get_corresponding_function({key: functions})
        else:
            agg_dictionary_compound_func[key] = get_corresponding_function({key: functions})
        
    # Agglomerates columns with single entry
    df_response = df.copy()
    if len(agg_dictionary_simple_func) > 0:
        df_response = df.groupby(groupby_cols).agg(agg_dictionary_simple_func).reset_index()
        
    # Second, Agglomerates columns with multiple parameters
    for col in agg_dictionary_compound_func.keys():
        fun = agg_dictionary_compound_func[col]
        df_temp = df.groupby(groupby_cols).apply(fun).to_frame().reset_index()
            
        # renames the new column
        df_temp.rename(columns = {0:col}, inplace=True)

        # Merges
        if isinstance(df_response, pd.Series):
            df_response = pd.DataFrame(df_response)
                
        df_response = df_response.merge(df_temp, on=groupby_cols)
            
    
    return(df_response)
    
    
# Organizer Method
def get_corresponding_function(function_declaration):
    '''
    Method that returns a function with a single parameter to insert into the groupby.
    
    If function is supported by the Pandas.GroupBy Scheme, will return a string for efficiency.
    '''
    
    attr = attr = list(function_declaration.keys())[0]
    functions = function_declaration[attr]
    name = functions[0]
    if len(functions) > 1:
        params = functions[1]
    
    # Sum
    if name == 'SUM':
        return('sum')
    
    # Average
    if name == 'MEAN':
        return('mean')
    
    # Frequency
    if name == 'FREQUENCY':
        return('count')
    
    # Returns a list of the values separated by the indicated character.  
    if name == 'CONCAT': 
        null_handling = params["NULL_HANDLING"].lower()
        sep = params["SEP"]
        if null_handling == "drop_na":
            fun = lambda s : sep.join(s[attr].dropna())
        else:
            raise Exception("Behaviour not implemented yet")
        return(fun)
    
    if name == 'WEIGHTED_MEAN': 
        weight = params["WEIGHT"]
        fun = lambda df : (df[weight]*df[attr]).sum() / df[weight].sum() 

        return(fun)
        

    raise ValueError(f'No implementation found for function: {name}. Please add it.')

