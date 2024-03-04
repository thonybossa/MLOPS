
import tensorflow as tf
import pandas as pd
from google.protobuf.json_format import MessageToDict

def get_records(dataset, num_records):
    
    '''Extrae registros del conjunto de datos dado.
    Args:
        dataset (TFRecordDataset): conjunto de datos guardado por ExampleGen
        num_records (int): número de registros para previsualizar
    '''    
    # initialize an empty list
    records = []
    
    # Use the `take()` method to specify how many records to get
    for tfrecord in dataset.take(num_records):
        
        # Get the numpy property of the tensor
        serialized_example = tfrecord.numpy()
        
        # Initialize a `tf.train.Example()` to read the serialized data
        example = tf.train.Example()
        
        # Read the example data (output is a protocol buffer message)
        example.ParseFromString(serialized_example)
        
        # convert the protocol bufffer message to a Python dictionary
        example_dict = (MessageToDict(example))
        
        # append to the records list
        records.append(example_dict)
        
    return records

def display_types(types):
    # Función auxiliar para renderizar DataFrames para los tipos de artefactos y ejecuciones
    table = {'id': [], 'name': []}
    for a_type in types:
        table['id'].append(a_type.id)
        table['name'].append(a_type.name)
    return pd.DataFrame(data=table)

def display_artifacts(store, artifacts, base_dir):
    # Función auxiliar para renderizar DataFrames para los artefactos de entrada
    table = {'artifact id': [], 'type': [], 'uri': []}
    for a in artifacts:
        table['artifact id'].append(a.id)
        artifact_type = store.get_artifact_types_by_id([a.type_id])[0]
        table['type'].append(artifact_type.name)
        table['uri'].append(a.uri.replace(base_dir, './'))
    return pd.DataFrame(data=table)

def display_properties(store, node):
    # Función auxiliar para renderizar DataFrames para las propiedades de artefactos y ejecuciones
    table = {'property': [], 'value': []}
    
    for k, v in node.properties.items():
        table['property'].append(k)
        table['value'].append(
            v.string_value if v.HasField('string_value') else v.int_value)
    
    for k, v in node.custom_properties.items():
        table['property'].append(k)
        table['value'].append(
            v.string_value if v.HasField('string_value') else v.int_value)
    
    return pd.DataFrame(data=table)
