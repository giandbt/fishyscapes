---
title: Submission
# subtitle: This is the demo site for Bulma Clean Theme
layout: page
show_sidebar: false
hide_footer: false
---
To test methods on the dynamic datasets of the benchmark, we require submission of executables. These may be saved models, binaries, docker images or source code. Any submitted method should take an rgb image as input and produce semantic segmentation aswell as pixelwise uncertainty scores. See below for an example of submitting a tensorflow saved model.

<a class="button is-primary" target="_blank" href="https://forms.gle/Rrc9nWuxsmks9CuX7">Submit your Model</a>

# Submit a Tensorflow Graph
Save your model following the [tensorflow guide](https://www.tensorflow.org/guide/saved_model) with the following specifications of its input and output:

```python
tf.saved_model.simple_save(
    <session object>,
    <export path>,
    inputs={'rgb': <your rgb input tensor>},
    outputs={'prediction': <semantic classification of the input image>,
             'anomaly_score': <anomaly score tensor>})
```
The anomaly score tensor has the same height and width as the input image and assigns for each pixel a `float32` score that is higher for higher probability of anomaly. You do not have to threshold anything as we will test the methods over all possible thresholds.

<article class="message is-warning">
  <div class="message-header">
    <p>Important</p>
  </div>
  <div class="message-body">
    The saved model does not contain any original code of yours, only the tensorflow compute graph defined by the code.
  </div>
</article>
