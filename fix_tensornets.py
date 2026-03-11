# Compatibility patch for tensornets with TensorFlow 2.x
# This adds the missing imports that tensornets expects from TensorFlow 1.x

import tensorflow as tf

# Add compatibility shims for tensornets
try:
    from tensorflow.python import keras
    from keras.applications.imagenet_utils import preprocess_input as imagenet_preprocess
    from keras.applications.imagenet_utils import decode_predictions as imagenet_decode
except ImportError:
    # For TensorFlow 2.x compatibility
    import tensorflow.keras as keras
    from tensorflow.keras.applications.imagenet_utils import preprocess_input as imagenet_preprocess
    from tensorflow.keras.applications.imagenet_utils import decode_predictions as imagenet_decode
    
print("tensornets compatibility initialized")

