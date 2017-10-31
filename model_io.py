from keras.models import model_from_json


class ModelIO(object):

    def save(self, model, structure_file_name="model.json", weights_file_name="model.h5"):
        model_json = model.to_json()
        with open(structure_file_name, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(weights_file_name)
        print("Saved model to disk")

    def load(self, structure_file_name="model.json", weights_file_name="model.h5"):
        # load json and create model
        json_file = open(structure_file_name, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(weights_file_name)
        print("Loaded model from disk")

        return loaded_model
