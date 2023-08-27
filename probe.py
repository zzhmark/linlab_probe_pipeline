import numpy as np

from probeinterface import Probe, ProbeGroup
from probeinterface.plotting import plot_probe, plot_probe_group
from probeinterface import generate_multi_columns_probe
from probeinterface import generate_linear_probe, generate_multi_shank
from probeinterface import combine_probes
from probeinterface import generate_dummy_probe
from probeinterface import write_probeinterface, read_probeinterface
from probeinterface import write_prb, read_prb

def my_probe():

    n = 64
    positions = np.zeros((n, 2))
    #for i in range(n):
  #      x = i // 10
  #      y = i % 10
 #       positions[i] = x, y
   # positions *= 20
   # positions[8:16, 1] -= 10

    positions[0] = 0, 0
    positions[1] = -3.1, 100
    positions[2] = -6.2, 200
    positions[3] = -9.3, 300
    positions[4] = -12.4, 400
    positions[5] = -15.5, 500
    positions[6] = -18.6, 600
    positions[7] = -21.7, 700
    positions[8] = -24.8, 1200
    positions[9] = -27.9, 1300
    positions[10] = 55, -50
    positions[11] = 51.9, 50
    positions[12] = 48.8, 150
    positions[13] = 45.7, 250
    positions[14] = 42.6, 350
    positions[15] = 39.5, 450
    positions[16] = 36.4, 550
    positions[17] = 33.3, 650
    positions[18] = 30.2, 750
    positions[19] = 27.1, 850
    positions[20] = 110, 0
    positions[21] = 106.9, 100
    positions[22] = 103.8, 200
    positions[23] = 100.7, 300
    positions[24] = 97.6, 400
    positions[25] = 94.5, 500
    positions[26] = 91.4, 600
    positions[27] = 88.3, 700
    positions[28] = 85.2, 800
    positions[29] = 82.1, 900
    positions[30] = 137.1, 0
    positions[31] = 140.2, 100
    positions[32] = 143.3, 200
    positions[33] = 146.4, 300
    positions[34] = 149.5, 400
    positions[35] = 152.6, 500
    positions[36] = 155.7, 600
    positions[37] = 158.8, 700
    positions[38] = 161.9, 800
    positions[39] = 165, 900
    positions[40] = 192.1, -50
    positions[41] = 195.2, 50
    positions[42] = 198.3, 150
    positions[43] = 201.4, 250
    positions[44] = 204.5, 350
    positions[45] = 207.6, 450
    positions[46] = 210.7, 550
    positions[47] = 213.8, 650
    positions[48] = 216.9, 750
    positions[49] = 220, 850
    positions[50] = 247.1, 0
    positions[51] = 250.2, 100
    positions[52] = 253.3, 200
    positions[53] = 256.4, 300
    positions[54] = 259.5, 400
    positions[55] = 262.6, 500
    positions[56] = 265.7, 600
    positions[57] = 268.8, 700
    positions[58] = 271.9, 800
    positions[59] = 275, 900
    positions[60] = 278.1, 1400
    positions[61] = 168.1, 1400
    positions[62] = 79, 1400
    positions[63] = -31, 1400

    probe_2d0 = Probe(ndim=2, si_units='um')
    probe_2d0.set_contacts(positions=positions, shapes='circle', shape_params={'radius': 5})

    probe_2d1 = probe_2d0.copy()
    probe_2d1.move([1000, 0])

    multi_shank = combine_probes([probe_2d0, probe_2d1])

    polygon = [(-31, -53.1), (281.2, -53.1), (281.2, 1003.1), (969, 1003.1), (969, -53.1), (1281.2, -53.1),
               (1281.2, 1500), (-31, 1500)]

    multi_shank.set_planar_contour(polygon)

    channel_indices = np.arange(128)

    channel_indices[0] = 41
    channel_indices[1] = 57
    channel_indices[2] = 43
    channel_indices[3] = 55
    channel_indices[4] = 45
    channel_indices[5] = 53
    channel_indices[6] = 47
    channel_indices[7] = 51
    channel_indices[8] = 16
    channel_indices[9] = 18
    channel_indices[10] = 31
    channel_indices[11] = 3
    channel_indices[12] = 33
    channel_indices[13] = 1
    channel_indices[14] = 35
    channel_indices[15] = 63
    channel_indices[16] = 37
    channel_indices[17] = 61
    channel_indices[18] = 39
    channel_indices[19] = 59
    channel_indices[20] = 21
    channel_indices[21] = 13
    channel_indices[22] = 23
    channel_indices[23] = 11
    channel_indices[24] = 25
    channel_indices[25] = 9
    channel_indices[26] = 27
    channel_indices[27] = 7
    channel_indices[28] = 29
    channel_indices[29] = 5
    channel_indices[30] = 15
    channel_indices[31] = 19
    channel_indices[32] = 52
    channel_indices[33] = 46
    channel_indices[34] = 54
    channel_indices[35] = 44
    channel_indices[36] = 56
    channel_indices[37] = 42
    channel_indices[38] = 58
    channel_indices[39] = 40
    channel_indices[40] = 60
    channel_indices[41] = 38
    channel_indices[42] = 62
    channel_indices[43] = 36
    channel_indices[44] = 0
    channel_indices[45] = 34
    channel_indices[46] = 2
    channel_indices[47] = 32
    channel_indices[48] = 4
    channel_indices[49] = 30
    channel_indices[50] = 6
    channel_indices[51] = 28
    channel_indices[52] = 8
    channel_indices[53] = 26
    channel_indices[54] = 10
    channel_indices[55] = 24
    channel_indices[56] = 12
    channel_indices[57] = 22
    channel_indices[58] = 14
    channel_indices[59] = 20
    channel_indices[60] = 48
    channel_indices[61] = 50
    channel_indices[62] = 17
    channel_indices[63] = 49
    channel_indices[64] = 105
    channel_indices[65] = 121
    channel_indices[66] = 107
    channel_indices[67] = 119
    channel_indices[68] = 109
    channel_indices[69] = 117
    channel_indices[70] = 111
    channel_indices[71] = 115
    channel_indices[72] = 80
    channel_indices[73] = 82
    channel_indices[74] = 95
    channel_indices[75] = 67
    channel_indices[76] = 97
    channel_indices[77] = 65
    channel_indices[78] = 99
    channel_indices[79] = 127
    channel_indices[80] = 101
    channel_indices[81] = 125
    channel_indices[82] = 103
    channel_indices[83] = 123
    channel_indices[84] = 85
    channel_indices[85] = 77
    channel_indices[86] = 87
    channel_indices[87] = 75
    channel_indices[88] = 89
    channel_indices[89] = 73
    channel_indices[90] = 91
    channel_indices[91] = 71
    channel_indices[92] = 93
    channel_indices[93] = 69
    channel_indices[94] = 79
    channel_indices[95] = 83
    channel_indices[96] = 116
    channel_indices[97] = 110
    channel_indices[98] = 118
    channel_indices[99] = 108
    channel_indices[100] = 120
    channel_indices[101] = 106
    channel_indices[102] = 122
    channel_indices[103] = 104
    channel_indices[104] = 124
    channel_indices[105] = 102
    channel_indices[106] = 126
    channel_indices[107] = 100
    channel_indices[108] = 64
    channel_indices[109] = 98
    channel_indices[110] = 66
    channel_indices[111] = 96
    channel_indices[112] = 68
    channel_indices[113] = 94
    channel_indices[114] = 70
    channel_indices[115] = 92
    channel_indices[116] = 72
    channel_indices[117] = 90
    channel_indices[118] = 74
    channel_indices[119] = 88
    channel_indices[120] = 76
    channel_indices[121] = 86
    channel_indices[122] = 78
    channel_indices[123] = 84
    channel_indices[124] = 112
    channel_indices[125] = 114
    channel_indices[126] = 81
    channel_indices[127] = 113

    multi_shank.set_device_channel_indices(channel_indices)

    return multi_shank


