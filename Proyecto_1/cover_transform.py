
import tensorflow as tf
import tensorflow_transform as tft

import cover_constants

# Importamos constantes y funciones definidas en el módulo cover_constants.
_SCALE_MINMAX_FEATURE_KEYS = cover_constants.SCALE_MINMAX_FEATURE_KEYS
_SCALE_01_FEATURE_KEYS = cover_constants.SCALE_01_FEATURE_KEYS
_SCALE_Z_FEATURE_KEYS = cover_constants.SCALE_Z_FEATURE_KEYS
_VOCAB_FEATURE_KEYS = cover_constants.VOCAB_FEATURE_KEYS
_HASH_STRING_FEATURE_KEYS = cover_constants.HASH_STRING_FEATURE_KEYS
_LABEL_KEY = cover_constants.LABEL_KEY
_transformed_name = cover_constants.transformed_name

# Definimos la función de preprocesamiento.
def preprocessing_fn(inputs):

    features_dict = {}

    # Escalamos las características utilizando la función scale_by_min_max.
    for feature in _SCALE_MINMAX_FEATURE_KEYS:
        data_col = inputs[feature] 
        features_dict[_transformed_name(feature)] = tft.scale_by_min_max(data_col)
        
    # Escalamos las características a un rango entre 0 y 1.
    for feature in _SCALE_01_FEATURE_KEYS:
        data_col = inputs[feature] 
        features_dict[_transformed_name(feature)] = tft.scale_to_0_1(data_col)

    # Escalamos las características utilizando la puntuación Z.
    for feature in _SCALE_Z_FEATURE_KEYS:
        data_col = inputs[feature] 
        features_dict[_transformed_name(feature)] = tft.scale_to_z_score(data_col)

    # Aplicamos un vocabulario a las características categóricas.
    for feature in _VOCAB_FEATURE_KEYS:
        data_col = inputs[feature] 
        features_dict[_transformed_name(feature)] = tft.compute_and_apply_vocabulary(data_col)

    # Convertimos las cadenas de caracteres en características numéricas mediante hashing.
    for feature in _HASH_STRING_FEATURE_KEYS:
        data_col = inputs[feature] 
        features_dict[_transformed_name(feature)] = tft.hash_strings(data_col, hash_buckets=10)

    features_dict[_LABEL_KEY] = inputs[_LABEL_KEY]

    return features_dict
