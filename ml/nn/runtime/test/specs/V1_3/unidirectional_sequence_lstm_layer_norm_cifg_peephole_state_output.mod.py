#
# Copyright (C) 2019 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Unidirectional Sequence LSTM Test:
# 3 Time Step, Layer Normalization, Cifg, Peephole, Projection, and No Clipping.
import copy

model = Model()

max_time = 3
n_batch = 2
n_input = 5
# n_cell and n_output have the same size when there is no projection.
n_cell = 4
n_output = 3

input = Input("input", "TENSOR_FLOAT32",
              "{%d, %d, %d}" % (max_time, n_batch, n_input))

input_to_input_weights = Input("input_to_input_weights", "TENSOR_FLOAT32",
                               "{0, 0}")
input_to_forget_weights = Input("input_to_forget_weights", "TENSOR_FLOAT32",
                                "{%d, %d}" % (n_cell, n_input))
input_to_cell_weights = Input("input_to_cell_weights", "TENSOR_FLOAT32",
                              "{%d, %d}" % (n_cell, n_input))
input_to_output_weights = Input("input_to_output_weights", "TENSOR_FLOAT32",
                                "{%d, %d}" % (n_cell, n_input))

recurrent_to_input_weights = Input("recurrent_to_intput_weights",
                                   "TENSOR_FLOAT32", "{0, 0}")
recurrent_to_forget_weights = Input("recurrent_to_forget_weights",
                                    "TENSOR_FLOAT32",
                                    "{%d, %d}" % (n_cell, n_output))
recurrent_to_cell_weights = Input("recurrent_to_cell_weights", "TENSOR_FLOAT32",
                                  "{%d, %d}" % (n_cell, n_output))
recurrent_to_output_weights = Input("recurrent_to_output_weights",
                                    "TENSOR_FLOAT32",
                                    "{%d, %d}" % (n_cell, n_output))

cell_to_input_weights = Input("cell_to_input_weights", "TENSOR_FLOAT32", "{0}")
cell_to_forget_weights = Input("cell_to_forget_weights", "TENSOR_FLOAT32",
                               "{%d}" % (n_cell))
cell_to_output_weights = Input("cell_to_output_weights", "TENSOR_FLOAT32",
                               "{%d}" % (n_cell))

input_gate_bias = Input("input_gate_bias", "TENSOR_FLOAT32", "{0}")
forget_gate_bias = Input("forget_gate_bias", "TENSOR_FLOAT32",
                         "{%d}" % (n_cell))
cell_gate_bias = Input("cell_gate_bias", "TENSOR_FLOAT32", "{%d}" % (n_cell))
output_gate_bias = Input("output_gate_bias", "TENSOR_FLOAT32",
                         "{%d}" % (n_cell))

projection_weights = Input("projection_weights", "TENSOR_FLOAT32",
                           "{%d,%d}" % (n_output, n_cell))
projection_bias = Input("projection_bias", "TENSOR_FLOAT32", "{0}")

output_state_in = Input("output_state_in", "TENSOR_FLOAT32",
                        "{%d, %d}" % (n_batch, n_output))
cell_state_in = Input("cell_state_in", "TENSOR_FLOAT32",
                      "{%d, %d}" % (n_batch, n_cell))

activation_param = Int32Scalar("activation_param", 4)  # Tanh
cell_clip_param = Float32Scalar("cell_clip_param", 0.)
proj_clip_param = Float32Scalar("proj_clip_param", 0.)
time_major_param = BoolScalar("time_major_param", True)

input_layer_norm_weights = Input("input_layer_norm_weights", "TENSOR_FLOAT32",
                                 "{0}")
forget_layer_norm_weights = Input("forget_layer_norm_weights", "TENSOR_FLOAT32",
                                  "{%d}" % n_cell)
cell_layer_norm_weights = Input("cell_layer_norm_weights", "TENSOR_FLOAT32",
                                "{%d}" % n_cell)
output_layer_norm_weights = Input("output_layer_norm_weights", "TENSOR_FLOAT32",
                                  "{%d}" % n_cell)

output = Output("output", "TENSOR_FLOAT32",
                "{%d, %d, %d}" % (max_time, n_batch, n_output))
output_state_out = Output("output_state_out", "TENSOR_FLOAT32",
                          "{%d, %d}" % (n_batch, n_output))
cell_state_out = Output("cell_state_out", "TENSOR_FLOAT32",
                        "{%d, %d}" % (n_batch, n_cell))

model = model.Operation(
    "UNIDIRECTIONAL_SEQUENCE_LSTM", input, input_to_input_weights,
    input_to_forget_weights, input_to_cell_weights, input_to_output_weights,
    recurrent_to_input_weights, recurrent_to_forget_weights,
    recurrent_to_cell_weights, recurrent_to_output_weights,
    cell_to_input_weights, cell_to_forget_weights, cell_to_output_weights,
    input_gate_bias, forget_gate_bias, cell_gate_bias, output_gate_bias,
    projection_weights, projection_bias, output_state_in, cell_state_in,
    activation_param, cell_clip_param, proj_clip_param, time_major_param,
    input_layer_norm_weights, forget_layer_norm_weights,
    cell_layer_norm_weights, output_layer_norm_weights).To(
        [output, output_state_out, cell_state_out])

# Example 1. Input in operand 0,
input0 = {
    input_to_input_weights: [],
    input_to_forget_weights: [
        -0.6, -0.1, 0.3, 0.2, 0.9, -0.5, -0.2, -0.4, 0.3, -0.8, -0.4, 0.3, -0.5,
        -0.4, -0.6, 0.3, -0.4, -0.6, -0.5, -0.5
    ],
    input_to_cell_weights: [
        -0.4, -0.3, -0.2, -0.1, -0.5, 0.5, -0.2, -0.3, -0.2, -0.6, 0.6, -0.1,
        -0.4, -0.3, -0.7, 0.7, -0.9, -0.5, 0.8, 0.6
    ],
    input_to_output_weights: [
        -0.8, -0.4, -0.2, -0.9, -0.1, -0.7, 0.3, -0.3, -0.8, -0.2, 0.6, -0.2,
        0.4, -0.7, -0.3, -0.5, 0.1, 0.5, -0.6, -0.4
    ],
    input_gate_bias: [],
    forget_gate_bias: [0.1, -0.3, -0.2, 0.1],
    cell_gate_bias: [-0.05, 0.72, 0.25, 0.08],
    output_gate_bias: [0.05, -0.01, 0.2, 0.1],
    recurrent_to_input_weights: [],
    recurrent_to_cell_weights: [
        -0.3, 0.2, 0.1, -0.3, 0.8, -0.08, -0.2, 0.3, 0.8, -0.6, -0.1, 0.2
    ],
    recurrent_to_forget_weights: [
        -0.5, -0.3, -0.5, -0.2, 0.6, 0.4, 0.9, 0.3, -0.1, 0.2, 0.5, 0.2
    ],
    recurrent_to_output_weights: [
        0.3, -0.1, 0.1, -0.2, -0.5, -0.7, -0.2, -0.6, -0.1, -0.4, -0.7, -0.2
    ],
    cell_to_input_weights: [],
    cell_to_forget_weights: [-0.02, -0.15, -0.25, -0.03],
    cell_to_output_weights: [0.1, -0.1, -0.5, 0.05],
    projection_weights: [
        -0.1, 0.2, 0.01, -0.2, 0.1, 0.5, 0.3, 0.08, 0.07, 0.2, -0.4, 0.2
    ],
    projection_bias: [],
    input_layer_norm_weights: [],
    forget_layer_norm_weights: [0.2, 0.2, 0.4, 0.3],
    cell_layer_norm_weights: [0.7, 0.2, 0.3, 0.8],
    output_layer_norm_weights: [0.6, 0.2, 0.2, 0.5]
}

test_input = [
    0.7, 0.8, 0.1, 0.2, 0.3, 0.3, 0.2, 0.9, 0.8, 0.1, 0.8, 0.1, 0.2, 0.4, 0.5,
    0.1, 0.5, 0.2, 0.4, 0.2, 0.2, 0.7, 0.7, 0.1, 0.7, 0.6, 0.9, 0.2, 0.5, 0.7
]

golden_output = [
    0.02129706,
    0.140816242,
    0.0112733059,
    -0.0226350538,
    0.0916948169,
    0.0769175813,
    0.0132302344,
    0.152308047,
    0.0346313119,
    -0.0269966982,
    0.149707705,
    0.094149217,
    -0.0123688057,
    0.165790111,
    0.0893077999,
    -0.0103429332,
    0.173016444,
    0.0720508844,
]

output0 = {
    output:
        golden_output,
    output_state_out:
        golden_output[(max_time - 1) * (n_batch * n_output):],
    cell_state_out: [
        -0.573662, 0.59525, 0.129295, 0.711027, -0.532303, 0.555613, 0.180099,
        0.784506
    ]
}

input0[input] = test_input
input0[output_state_in] = [0 for _ in range(n_batch * n_output)]
input0[cell_state_in] = [0 for _ in range(n_batch * n_cell)]

Example((input0, output0)).AddVariations("relaxed", "float16")
