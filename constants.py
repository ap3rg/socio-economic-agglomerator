import os

source_shape_file = os.path.join("/","Users","andreaparra","Dropbox","4_Work","DataLamaCovid","projects","bogota","data","censo_bogota","shape_files","consolidado", "consolidado.shp")

# Method of grouping for geometry. Overlaps or intersects
method = 'intersects'

variable_meaning = {'CODIGO_MZN': 'Codigo Manzana',
                    'SHAPE_AREA': 'Area',
                    'geometry': 'Geometria',
                    'CRTO_P_PER': 'Numero promedio de cuartos por persona',
                    'DORM_P_PER': 'Numero promedio de cuartos por persona',
                    'NUM_HOG': 'Numero de hogares',
                    'EE_PERCNT': 'Porcentaje de viviendas con servicio de energia',
                    'ACU_PERCNT': 'Porcentaje de viviendas con servicio de acueducto',
                    'ALC_PERCNT': 'Porcentaje de viviendas con servicio de alcatarillado',
                    'INT_PERCNT': 'Porcentaje de viviendas con servicio de internet',
                    'ESTRATO': 'Estrato',
                    'NUM_VIV': 'Numero de viviendas',
                    'MJR_PERCNT': 'Porcentaje de mujeres',
                    'HOM_PERCNT': 'Porcentaje de hombres',
                    'ALF_PERCNT': 'Porcentaje de personas alfabetas',
                    'MCF_PERCNT': 'Porcentaje de personas mujeres cabeza de hogar',
                    'NUM_PER': 'Numero de personas',
                    'VULNER': 'Vulnerabilidad categorica',
                    'VULNER_NUM': 'Vulnerabilidad numerica',
                    'IPM': 'Indice de pobreza multidimencional'}

variable_aggr = {'CODIGO_MZN': ['CONCAT', {'NULL_HANDLING': 'DROP_NA',
                                           'SEP': '|'}], 
                 'SHAPE_AREA': ['SUM'],
                 'CRTO_P_PER': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'DORM_P_PER': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'NUM_HOG': ['SUM'],
                 'EE_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_VIV'}],
                 'ACU_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_VIV'}],
                 'ALC_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_VIV'}],
                 'INT_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_VIV'}],
                 'ESTRATO': ['MEAN'],
                 'NUM_VIV': ['SUM'],
                 'MJR_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'HOM_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'ALF_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'MCF_PERCNT': ['WEIGHTED_MEAN', {'WEIGHT': 'NUM_PER'}],
                 'NUM_PER': ['SUM'],
                 'VULNER_NUM': ['MEAN'],
                 'IPM': ['MEAN']}
                
VULNER_DICT = {'Vulnerabilidad media-baja': 2,
                'Vulnerabilidad baja': 1,
                'Vulnerabilidad media': 3, 
                'Vulnerabilidad media-alta': 4,
                'Vulnerabilidad alta': 5,
                None: None}