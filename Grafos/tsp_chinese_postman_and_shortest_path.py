import math
import networkx as nx
import matplotlib.pyplot as plt

def read_tsp_file(file_content):
    """
    Reads a TSP file (in the format provided) and creates a graph with Euclidean distances as edge weights.

    Parameters:
    - file_content: The content of the TSP file as a string.

    Returns:
    - G: A NetworkX graph with nodes and edges based on Euclidean distances between points.
    """
    G = nx.Graph()
    lines = file_content.strip().split("\n")
    
    # Read node coordinates
    node_coords = {}
    in_section = False
    for line in lines:
        if line.startswith("NODE_COORD_SECTION"):
            in_section = True
            continue
        if in_section:
            if line.startswith("EOF"):
                break
            parts = line.split()
            node_id = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            node_coords[node_id] = (x, y)

    # Add nodes and edges to the graph
    for node1, (x1, y1) in node_coords.items():
        G.add_node(node1, pos=(x1, y1))  # Add node with its coordinates as attribute
        for node2, (x2, y2) in node_coords.items():
            if node1 < node2:  # Avoid duplicates
                weight = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Euclidean distance
                G.add_edge(node1, node2, weight=weight)

    return G

# Example of how to use this function with your provided data
file_content_lin318 = """
NODE_COORD_SECTION
1 63 71
2 94 71
3 142 370
4 173 1276
5 205 1213
6 213 69
7 244 69
8 276 630
9 283 732
10 362 69
11 394 69
12 449 370
13 480 1276
14 512 1213
15 528 157
16 583 630
17 591 732
18 638 654
19 638 496
20 638 314
21 638 142
22 669 142
23 677 315
24 677 496
25 677 654
26 709 654
27 709 496
28 709 315
29 701 142
30 764 220
31 811 189
32 843 173
33 858 370
34 890 1276
35 921 1213
36 992 630
37 1000 732
38 1197 1276
39 1228 1213
40 1276 205
41 1299 630
42 1307 732
43 1362 654
44 1362 496
45 1362 291
46 1425 654
47 1425 496
48 1425 291
49 1417 173
50 1488 291
51 1488 496
52 1488 654
53 1551 654
54 1551 496
55 1551 291
56 1614 291
57 1614 496
58 1614 654
59 1732 189
60 1811 1276
61 1843 1213
62 1913 630
63 1921 732
64 2087 370
65 2118 1276
66 2150 1213
67 2189 205
68 2220 189
69 2220 630
70 2228 732
71 2244 142
72 2276 315
73 2276 496
74 2276 654
75 2315 654
76 2315 496
77 2315 315
78 2331 142
79 2346 315
80 2346 496
81 2346 654
82 2362 142
83 2402 157
84 2402 220
85 2480 142
86 2496 370
87 2528 1276
88 2559 1213
89 2630 630
90 2638 732
91 2756 69
92 2787 69
93 2803 370
94 2835 1276
95 2866 1213
96 2906 69
97 2937 69
98 2937 630
99 2945 732
100 3016 1276
101 3055 69
102 3087 69
103 606 220
104 1165 370
105 1780 370
106 63 1402
107 94 1402
108 142 1701
109 173 2607
110 205 2544
111 213 1400
112 244 1400
113 276 1961
114 283 2063
115 362 1400
116 394 1400
117 449 1701
118 480 2607
119 512 2544
120 528 1488
121 583 1961
122 591 2063
123 638 1985
124 638 1827
125 638 1645
126 638 1473
127 669 1473
128 677 1646
129 677 1827
130 677 1985
131 709 1985
132 709 1827
133 709 1646
134 701 1473
135 764 1551
136 811 1520
137 843 1504
138 858 1701
139 890 2607
140 921 2544
141 992 1961
142 1000 2063
143 1197 2607
144 1228 2544
145 1276 1536
146 1299 1961
147 1307 2063
148 1362 1985
149 1362 1827
150 1362 1622
151 1425 1985
152 1425 1827
153 1425 1622
154 1417 1504
155 1488 1622
156 1488 1827
157 1488 1985
158 1551 1985
159 1551 1827
160 1551 1622
161 1614 1622
162 1614 1827
163 1614 1985
164 1732 1520
165 1811 2607
166 1843 2544
167 1913 1961
168 1921 2063
169 2087 1701
170 2118 2607
171 2150 2544
172 2189 1536
173 2220 1520
174 2220 1961
175 2228 2063
176 2244 1473
177 2276 1646
178 2276 1827
179 2276 1985
180 2315 1985
181 2315 1827
182 2315 1646
183 2331 1473
184 2346 1646
185 2346 1827
186 2346 1985
187 2362 1473
188 2402 1488
189 2402 1551
190 2480 1473
191 2496 1701
192 2528 2607
193 2559 2544
194 2630 1961
195 2638 2063
196 2756 1400
197 2787 1400
198 2803 1701
199 2835 2607
200 2866 2544
201 2906 1400
202 2937 1400
203 2937 1961
204 2945 2063
205 3016 2607
206 3055 1400
207 3087 1400
208 606 1551
209 1165 1701
210 1780 1701
211 63 2733
212 94 2733
213 142 3032
214 173 3938
215 205 3875
216 213 2731
217 244 2731
218 276 3292
219 283 3394
220 362 2731
221 394 2731
222 449 3032
223 480 3938
224 512 3875
225 528 2819
226 583 3292
227 591 3394
228 638 3316
229 638 3158
230 638 2976
231 638 2804
232 669 2804
233 677 2977
234 677 3158
235 677 3316
236 709 3316
237 709 3158
238 709 2977
239 701 2804
240 764 2882
241 811 2851
242 843 2835
243 858 3032
244 890 3938
245 921 3875
246 992 3292
247 1000 3394
248 1197 3938
249 1228 3875
250 1276 2867
251 1299 3292
252 1307 3394
253 1362 3316
254 1362 3158
255 1362 2953
256 1425 3316
257 1425 3158
258 1425 2953
259 1417 2835
260 1488 2953
261 1488 3158
262 1488 3316
263 1551 3316
264 1551 3158
265 1551 2953
266 1614 2953
267 1614 3158
268 1614 3316
269 1732 2851
270 1811 3938
271 1843 3875
272 1913 3292
273 1921 3394
274 2087 3032
275 2118 3938
276 2150 3875
277 2189 2867
278 2220 2851
279 2220 3292
280 2228 3394
281 2244 2804
282 2276 2977
283 2276 3158
284 2276 3316
285 2315 3316
286 2315 3158
287 2315 2977
288 2331 2804
289 2346 2977
290 2346 3158
291 2346 3316
292 2362 2804
293 2402 2819
294 2402 2882
295 2480 2804
296 2496 3032
297 2528 3938
298 2559 3875
299 2630 3292
300 2638 3394
301 2756 2731
302 2787 2731
303 2803 3032
304 2835 3938
305 2866 3875
306 2906 2731
307 2937 2731
308 2937 3292
309 2945 3394
310 3016 3938
311 3055 2731
312 3087 2731
313 606 2882
314 1165 3032
315 1780 3032
316 1417 -79
317 1496 -79
318 1693 4055
EOF
"""

file_content_kroA100 = """
NODE_COORD_SECTION
1 1380 939
2 2848 96
3 3510 1671
4 457 334
5 3888 666
6 984 965
7 2721 1482
8 1286 525
9 2716 1432
10 738 1325
11 1251 1832
12 2728 1698
13 3815 169
14 3683 1533
15 1247 1945
16 123 862
17 1234 1946
18 252 1240
19 611 673
20 2576 1676
21 928 1700
22 53 857
23 1807 1711
24 274 1420
25 2574 946
26 178 24
27 2678 1825
28 1795 962
29 3384 1498
30 3520 1079
31 1256 61
32 1424 1728
33 3913 192
34 3085 1528
35 2573 1969
36 463 1670
37 3875 598
38 298 1513
39 3479 821
40 2542 236
41 3955 1743
42 1323 280
43 3447 1830
44 2936 337
45 1621 1830
46 3373 1646
47 1393 1368
48 3874 1318
49 938 955
50 3022 474
51 2482 1183
52 3854 923
53 376 825
54 2519 135
55 2945 1622
56 953 268
57 2628 1479
58 2097 981
59 890 1846
60 2139 1806
61 2421 1007
62 2290 1810
63 1115 1052
64 2588 302
65 327 265
66 241 341
67 1917 687
68 2991 792
69 2573 599
70 19 674
71 3911 1673
72 872 1559
73 2863 558
74 929 1766
75 839 620
76 3893 102
77 2178 1619
78 3822 899
79 378 1048
80 1178 100
81 2599 901
82 3416 143
83 2961 1605
84 611 1384
85 3113 885
86 2597 1830
87 2586 1286
88 161 906
89 1429 134
90 742 1025
91 1625 1651
92 1187 706
93 1787 1009
94 22 987
95 3640 43
96 3756 882
97 776 392
98 1724 1642
99 198 1810
100 3950 1558
EOF
"""

file_content_pcb442 = """
NODE_COORD_SECTION
1 2.00000e+02 4.00000e+02
2 2.00000e+02 5.00000e+02
3 2.00000e+02 6.00000e+02
4 2.00000e+02 7.00000e+02
5 2.00000e+02 8.00000e+02
6 2.00000e+02 9.00000e+02
7 2.00000e+02 1.00000e+03
8 2.00000e+02 1.10000e+03
9 2.00000e+02 1.20000e+03
10 2.00000e+02 1.30000e+03
11 2.00000e+02 1.40000e+03
12 2.00000e+02 1.50000e+03
13 2.00000e+02 1.60000e+03
14 2.00000e+02 1.70000e+03
15 2.00000e+02 1.80000e+03
16 2.00000e+02 1.90000e+03
17 2.00000e+02 2.00000e+03
18 2.00000e+02 2.10000e+03
19 2.00000e+02 2.20000e+03
20 2.00000e+02 2.30000e+03
21 2.00000e+02 2.40000e+03
22 2.00000e+02 2.50000e+03
23 2.00000e+02 2.60000e+03
24 2.00000e+02 2.70000e+03
25 2.00000e+02 2.80000e+03
26 2.00000e+02 2.90000e+03
27 2.00000e+02 3.00000e+03
28 2.00000e+02 3.10000e+03
29 2.00000e+02 3.20000e+03
30 2.00000e+02 3.30000e+03
31 2.00000e+02 3.40000e+03
32 2.00000e+02 3.50000e+03
33 2.00000e+02 3.60000e+03
34 3.00000e+02 4.00000e+02
35 3.00000e+02 5.00000e+02
36 3.00000e+02 6.00000e+02
37 3.00000e+02 7.00000e+02
38 3.00000e+02 8.00000e+02
39 3.00000e+02 9.00000e+02
40 3.00000e+02 1.00000e+03
41 3.00000e+02 1.10000e+03
42 3.00000e+02 1.20000e+03
43 3.00000e+02 1.30000e+03
44 3.00000e+02 1.40000e+03
45 3.00000e+02 1.50000e+03
46 3.00000e+02 1.60000e+03
47 3.00000e+02 1.70000e+03
48 3.00000e+02 1.80000e+03
49 3.00000e+02 1.90000e+03
50 3.00000e+02 2.00000e+03
51 3.00000e+02 2.10000e+03
52 3.00000e+02 2.20000e+03
53 3.00000e+02 2.30000e+03
54 3.00000e+02 2.40000e+03
55 3.00000e+02 2.50000e+03
56 3.00000e+02 2.60000e+03
57 3.00000e+02 2.70000e+03
58 3.00000e+02 2.80000e+03
59 3.00000e+02 2.90000e+03
60 3.00000e+02 3.00000e+03
61 3.00000e+02 3.10000e+03
62 3.00000e+02 3.20000e+03
63 3.00000e+02 3.30000e+03
64 3.00000e+02 3.40000e+03
65 3.00000e+02 3.50000e+03
66 4.00000e+02 4.00000e+02
67 4.00000e+02 5.00000e+02
68 4.00000e+02 6.00000e+02
69 4.00000e+02 7.00000e+02
70 4.00000e+02 8.00000e+02
71 4.00000e+02 9.00000e+02
72 4.00000e+02 1.00000e+03
73 4.00000e+02 1.10000e+03
74 4.00000e+02 1.20000e+03
75 4.00000e+02 1.30000e+03
76 4.00000e+02 1.40000e+03
77 4.00000e+02 1.50000e+03
78 4.00000e+02 1.60000e+03
79 4.00000e+02 1.70000e+03
80 4.00000e+02 1.80000e+03
81 4.00000e+02 1.90000e+03
82 4.00000e+02 2.00000e+03
83 4.00000e+02 2.10000e+03
84 4.00000e+02 2.20000e+03
85 4.00000e+02 2.30000e+03
86 4.00000e+02 2.40000e+03
87 4.00000e+02 2.50000e+03
88 4.00000e+02 2.60000e+03
89 4.00000e+02 2.70000e+03
90 4.00000e+02 2.80000e+03
91 4.00000e+02 2.90000e+03
92 4.00000e+02 3.00000e+03
93 4.00000e+02 3.10000e+03
94 4.00000e+02 3.20000e+03
95 4.00000e+02 3.30000e+03
96 4.00000e+02 3.40000e+03
97 4.00000e+02 3.50000e+03
98 4.00000e+02 3.60000e+03
99 5.00000e+02 1.50000e+03
100 5.00000e+02 1.82900e+03
101 5.00000e+02 3.10000e+03
102 6.00000e+02 4.00000e+02
103 7.00000e+02 3.00000e+02
104 7.00000e+02 6.00000e+02
105 7.00000e+02 1.50000e+03
106 7.00000e+02 1.60000e+03
107 7.00000e+02 1.80000e+03
108 7.00000e+02 2.10000e+03
109 7.00000e+02 2.40000e+03
110 7.00000e+02 2.70000e+03
111 7.00000e+02 3.00000e+03
112 7.00000e+02 3.30000e+03
113 7.00000e+02 3.60000e+03
114 8.00000e+02 3.00000e+02
115 8.00000e+02 6.00000e+02
116 8.00000e+02 1.03000e+03
117 8.00000e+02 1.50000e+03
118 8.00000e+02 1.80000e+03
119 8.00000e+02 2.10000e+03
120 8.00000e+02 2.40000e+03
121 8.00000e+02 2.60000e+03
122 8.00000e+02 2.70000e+03
123 8.00000e+02 3.00000e+03
124 8.00000e+02 3.30000e+03
125 8.00000e+02 3.60000e+03
126 9.00000e+02 3.00000e+02
127 9.00000e+02 6.00000e+02
128 9.00000e+02 1.50000e+03
129 9.00000e+02 1.80000e+03
130 9.00000e+02 2.10000e+03
131 9.00000e+02 2.40000e+03
132 9.00000e+02 2.70000e+03
133 9.00000e+02 3.00000e+03
134 9.00000e+02 3.30000e+03
135 9.00000e+02 3.60000e+03
136 1.00000e+03 3.00000e+02
137 1.00000e+03 6.00000e+02
138 1.00000e+03 1.10000e+03
139 1.00000e+03 1.50000e+03
140 1.00000e+03 1.62900e+03
141 1.00000e+03 1.80000e+03
142 1.00000e+03 2.10000e+03
143 1.00000e+03 2.40000e+03
144 1.00000e+03 2.60000e+03
145 1.00000e+03 2.70000e+03
146 1.00000e+03 3.00000e+03
147 1.00000e+03 3.30000e+03
148 1.00000e+03 3.60000e+03
149 1.10000e+03 3.00000e+02
150 1.10000e+03 6.00000e+02
151 1.10000e+03 7.00000e+02
152 1.10000e+03 9.00000e+02
153 1.10000e+03 1.50000e+03
154 1.10000e+03 1.80000e+03
155 1.10000e+03 2.10000e+03
156 1.10000e+03 2.40000e+03
157 1.10000e+03 2.70000e+03
158 1.10000e+03 3.00000e+03
159 1.10000e+03 3.30000e+03
160 1.10000e+03 3.60000e+03
161 1.20000e+03 3.00000e+02
162 1.20000e+03 6.00000e+02
163 1.20000e+03 1.50000e+03
164 1.20000e+03 1.70000e+03
165 1.20000e+03 1.80000e+03
166 1.20000e+03 2.10000e+03
167 1.20000e+03 2.40000e+03
168 1.20000e+03 2.70000e+03
169 1.20000e+03 3.00000e+03
170 1.20000e+03 3.30000e+03
171 1.20000e+03 3.60000e+03
172 1.30000e+03 3.00000e+02
173 1.30000e+03 6.00000e+02
174 1.30000e+03 7.00000e+02
175 1.30000e+03 1.13000e+03
176 1.30000e+03 1.50000e+03
177 1.30000e+03 1.80000e+03
178 1.30000e+03 2.10000e+03
179 1.30000e+03 2.20000e+03
180 1.30000e+03 2.40000e+03
181 1.30000e+03 2.70000e+03
182 1.30000e+03 3.00000e+03
183 1.30000e+03 3.30000e+03
184 1.30000e+03 3.60000e+03
185 1.40000e+03 3.00000e+02
186 1.40000e+03 6.00000e+02
187 1.40000e+03 9.30000e+02
188 1.40000e+03 1.50000e+03
189 1.40000e+03 1.80000e+03
190 1.40000e+03 2.00000e+03
191 1.40000e+03 2.10000e+03
192 1.40000e+03 2.40000e+03
193 1.40000e+03 2.50000e+03
194 1.40000e+03 2.70000e+03
195 1.40000e+03 2.82000e+03
196 1.40000e+03 2.90000e+03
197 1.40000e+03 3.00000e+03
198 1.40000e+03 3.30000e+03
199 1.40000e+03 3.60000e+03
200 1.50000e+03 1.50000e+03
201 1.50000e+03 1.80000e+03
202 1.50000e+03 1.90000e+03
203 1.50000e+03 2.10000e+03
204 1.50000e+03 2.40000e+03
205 1.50000e+03 2.70000e+03
206 1.50000e+03 2.80000e+03
207 1.50000e+03 2.86000e+03
208 1.50000e+03 3.00000e+03
209 1.50000e+03 3.30000e+03
210 1.50000e+03 3.60000e+03
211 1.60000e+03 1.10000e+03
212 1.60000e+03 1.30000e+03
213 1.60000e+03 1.50000e+03
214 1.60000e+03 1.80000e+03
215 1.60000e+03 2.10000e+03
216 1.60000e+03 2.40000e+03
217 1.60000e+03 2.70000e+03
218 1.60000e+03 3.00000e+03
219 1.60000e+03 3.30000e+03
220 1.60000e+03 3.60000e+03
221 1.70000e+03 1.20000e+03
222 1.70000e+03 1.50000e+03
223 1.70000e+03 1.80000e+03
224 1.70000e+03 2.10000e+03
225 1.70000e+03 2.40000e+03
226 1.70000e+03 3.60000e+03
227 1.80000e+03 3.00000e+02
228 1.80000e+03 6.00000e+02
229 1.80000e+03 1.23000e+03
230 1.80000e+03 1.50000e+03
231 1.80000e+03 1.80000e+03
232 1.80000e+03 2.10000e+03
233 1.80000e+03 2.40000e+03
234 1.90000e+03 3.00000e+02
235 1.90000e+03 6.00000e+02
236 1.90000e+03 3.00000e+03
237 1.90000e+03 3.52000e+03
238 2.00000e+03 3.00000e+02
239 2.00000e+03 3.70000e+02
240 2.00000e+03 6.00000e+02
241 2.00000e+03 8.00000e+02
242 2.00000e+03 9.00000e+02
243 2.00000e+03 1.00000e+03
244 2.00000e+03 1.10000e+03
245 2.00000e+03 1.20000e+03
246 2.00000e+03 1.30000e+03
247 2.00000e+03 1.40000e+03
248 2.00000e+03 1.50000e+03
249 2.00000e+03 1.60000e+03
250 2.00000e+03 1.70000e+03
251 2.00000e+03 1.80000e+03
252 2.00000e+03 1.90000e+03
253 2.00000e+03 2.00000e+03
254 2.00000e+03 2.10000e+03
255 2.00000e+03 2.20000e+03
256 2.00000e+03 2.30000e+03
257 2.00000e+03 2.40000e+03
258 2.00000e+03 2.50000e+03
259 2.00000e+03 2.60000e+03
260 2.00000e+03 2.70000e+03
261 2.00000e+03 2.80000e+03
262 2.00000e+03 2.90000e+03
263 2.00000e+03 3.00000e+03
264 2.00000e+03 3.10000e+03
265 2.00000e+03 3.50000e+03
266 2.10000e+03 3.00000e+02
267 2.10000e+03 6.00000e+02
268 2.10000e+03 3.20000e+03
269 2.20000e+03 3.00000e+02
270 2.20000e+03 4.69000e+02
271 2.20000e+03 6.00000e+02
272 2.20000e+03 3.20000e+03
273 2.30000e+03 3.00000e+02
274 2.30000e+03 6.00000e+02
275 2.30000e+03 3.40000e+03
276 2.40000e+03 3.00000e+02
277 2.40000e+03 6.00000e+02
278 2.40000e+03 2.10000e+03
279 2.50000e+03 3.00000e+02
280 2.50000e+03 8.00000e+02
281 2.60000e+03 4.00000e+02
282 2.60000e+03 5.00000e+02
283 2.60000e+03 8.00000e+02
284 2.60000e+03 9.00000e+02
285 2.60000e+03 1.00000e+03
286 2.60000e+03 1.10000e+03
287 2.60000e+03 1.20000e+03
288 2.60000e+03 1.30000e+03
289 2.60000e+03 1.40000e+03
290 2.60000e+03 1.50000e+03
291 2.60000e+03 1.60000e+03
292 2.60000e+03 1.70000e+03
293 2.60000e+03 1.80000e+03
294 2.60000e+03 1.90000e+03
295 2.60000e+03 2.00000e+03
296 2.60000e+03 2.10000e+03
297 2.60000e+03 2.20000e+03
298 2.60000e+03 2.30000e+03
299 2.60000e+03 2.40000e+03
300 2.60000e+03 2.50000e+03
301 2.60000e+03 2.60000e+03
302 2.60000e+03 2.70000e+03
303 2.60000e+03 2.80000e+03
304 2.60000e+03 2.90000e+03
305 2.60000e+03 3.00000e+03
306 2.60000e+03 3.10000e+03
307 2.60000e+03 3.40000e+03
308 2.70000e+03 7.00000e+02
309 2.70000e+03 8.00000e+02
310 2.70000e+03 9.00000e+02
311 2.70000e+03 1.00000e+03
312 2.70000e+03 1.10000e+03
313 2.70000e+03 1.20000e+03
314 2.70000e+03 1.30000e+03
315 2.70000e+03 1.40000e+03
316 2.70000e+03 1.50000e+03
317 2.70000e+03 1.60000e+03
318 2.70000e+03 1.70000e+03
319 2.70000e+03 1.80000e+03
320 2.70000e+03 1.90000e+03
321 2.70000e+03 2.00000e+03
322 2.70000e+03 2.10000e+03
323 2.70000e+03 2.20000e+03
324 2.70000e+03 2.30000e+03
325 2.70000e+03 2.50000e+03
326 2.70000e+03 2.60000e+03
327 2.70000e+03 2.70000e+03
328 2.70000e+03 2.80000e+03
329 2.70000e+03 2.90000e+03
330 2.70000e+03 3.00000e+03
331 2.70000e+03 3.10000e+03
332 2.70000e+03 3.20000e+03
333 2.70000e+03 3.30000e+03
334 2.70000e+03 3.40000e+03
335 2.70000e+03 3.50000e+03
336 2.70000e+03 3.60000e+03
337 2.70000e+03 3.70000e+03
338 2.70000e+03 3.80000e+03
339 2.80000e+03 9.00000e+02
340 2.80000e+03 1.13000e+03
341 2.90000e+03 4.00000e+02
342 2.90000e+03 5.00000e+02
343 2.90000e+03 1.40000e+03
344 2.90000e+03 2.40000e+03
345 2.90000e+03 3.00000e+03
346 3.00000e+03 7.00000e+02
347 3.00000e+03 8.00000e+02
348 3.00000e+03 9.00000e+02
349 3.00000e+03 1.00000e+03
350 3.00000e+03 1.10000e+03
351 3.00000e+03 1.20000e+03
352 3.00000e+03 1.30000e+03
353 3.00000e+03 1.50000e+03
354 3.00000e+03 1.60000e+03
355 3.00000e+03 1.70000e+03
356 3.00000e+03 1.80000e+03
357 3.00000e+03 1.90000e+03
358 3.00000e+03 2.00000e+03
359 3.00000e+03 2.10000e+03
360 3.00000e+03 2.20000e+03
361 3.00000e+03 2.30000e+03
362 3.00000e+03 2.50000e+03
363 3.00000e+03 2.60000e+03
364 3.00000e+03 2.70000e+03
365 3.00000e+03 2.80000e+03
366 3.00000e+03 2.90000e+03
367 3.00000e+03 3.00000e+03
368 3.00000e+03 3.10000e+03
369 3.00000e+03 3.20000e+03
370 3.00000e+03 3.30000e+03
371 3.00000e+03 3.40000e+03
372 3.00000e+03 3.50000e+03
373 3.00000e+03 3.60000e+03
374 3.00000e+03 3.70000e+03
375 3.00000e+03 3.80000e+03
376 1.50000e+02 3.50000e+03
377 1.50000e+02 3.55000e+03
378 4.69000e+02 2.55000e+03
379 4.69000e+02 3.35000e+03
380 4.69000e+02 3.45000e+03
381 5.40000e+02 2.33000e+03
382 5.40000e+02 2.43000e+03
383 6.20000e+02 3.65000e+03
384 6.20000e+02 3.70900e+03
385 7.50000e+02 2.55000e+03
386 8.50000e+02 5.20000e+02
387 8.50000e+02 7.00000e+02
388 8.50000e+02 2.28000e+03
389 9.39000e+02 7.40000e+02
390 9.50000e+02 2.22000e+03
391 9.10000e+02 2.60000e+03
392 1.05000e+03 1.05000e+03
393 1.15000e+03 1.35000e+03
394 1.17000e+03 2.28000e+03
395 1.22000e+03 2.21000e+03
396 1.35000e+03 7.50000e+02
397 1.35000e+03 1.70000e+03
398 1.35000e+03 2.14000e+03
399 1.45000e+03 7.70000e+02
400 1.55000e+03 3.00000e+02
401 1.55000e+03 5.00000e+02
402 1.55000e+03 1.85000e+03
403 1.65000e+03 1.05000e+03
404 1.69000e+03 2.68000e+03
405 1.71000e+03 3.10000e+02
406 1.71000e+03 5.10000e+02
407 1.75000e+03 7.50000e+02
408 1.79000e+03 2.58000e+03
409 1.72000e+03 2.61000e+03
410 1.79000e+03 3.33000e+03
411 1.72000e+03 3.40900e+03
412 1.82900e+03 2.70000e+03
413 1.82900e+03 2.80000e+03
414 1.82900e+03 3.45000e+03
415 2.06000e+03 1.65000e+03
416 2.05000e+03 3.15000e+03
417 2.17000e+03 1.90000e+03
418 2.11000e+03 2.00000e+03
419 2.12000e+03 2.75000e+03
420 2.15000e+03 3.25000e+03
421 2.29000e+03 1.40000e+03
422 2.22000e+03 2.82000e+03
423 2.28000e+03 3.25000e+03
424 2.39000e+03 1.30000e+03
425 2.32000e+03 1.50000e+03
426 2.45000e+03 7.10000e+02
427 2.62000e+03 3.65000e+03
428 2.75000e+03 5.20000e+02
429 2.76000e+03 2.36000e+03
430 2.85000e+03 2.20000e+03
431 2.85000e+03 2.70000e+03
432 2.85000e+03 3.35000e+03
433 2.93000e+03 9.50000e+02
434 2.95000e+03 1.75000e+03
435 2.95000e+03 2.05000e+03
436 5.20000e+02 3.20000e+03
437 2.30000e+03 3.50000e+03
438 2.32000e+03 3.15000e+03
439 5.30000e+02 2.10000e+03
440 2.55000e+03 7.10000e+02
441 7.50000e+02 4.90000e+02
442 0.00000e+00 0.00000e+00
EOF
"""

# Read the graph from the TSP data
G = read_tsp_file(file_content_kroA100) ## change here to read the desired file

# 1. TSP (Traveling Salesman Problem) using approximation
# TSP aims to find the shortest possible route that visits each node exactly once and returns to the starting node.
# NetworkX provides an approximation algorithm that uses a minimum spanning tree to provide a near-optimal solution
# which is guaranteed to be within a factor of 2 of the optimal path length.
tsp_path = nx.approximation.traveling_salesman_problem(G, weight='weight')

# 2. CPP (Chinese Postman Problem) for non-Eulerian graphs
# The Chinese Postman Problem requires that every edge be visited at least once.
# For non-Eulerian graphs (which don't have an Eulerian circuit), we first 'eulerize' the graph,
# which means we add duplicate edges to create an Eulerian circuit, allowing all edges to be traversed.
eulerian_graph = nx.eulerize(G)

# Generate the Eulerian circuit, which is now possible after eulerizing the graph.
cpp_circuit = list(nx.eulerian_circuit(eulerian_graph, source=1))

# 3. Shortest Path using A* algorithm
# A* algorithm finds the shortest path from node 1 to last node.
# It uses a heuristic to guide the search process, making it more efficient than Dijkstra in certain cases.
shortest_path = nx.astar_path(G, source=1, target=max(G.nodes), heuristic=lambda a, b: abs(a - b), weight='weight')

# Display results with explanations
def display_results(tsp_path, cpp_circuit, shortest_path):
    # Traveling Salesman Problem (TSP) result
    print("1. Traveling Salesman Problem (TSP) Approximate Path:")
    print(f"   Path: {tsp_path}")
    print(f"   Total Cost: {sum(G[tsp_path[i]][tsp_path[i+1]]['weight'] for i in range(len(tsp_path)-1))}")

    # Chinese Postman Problem (CPP) result
    print("\n2. Chinese Postman Problem (Eulerian Circuit):")
    # print("   Circuit: ", [edge for edge in cpp_circuit])
    # To calculate the total cost of the CPP, we sum the weights of the edges in the Eulerian circuit.
    # We read the weights directly from the original graph G to ensure accuracy.
    cpp_total_cost = sum(G[u][v]['weight'] for u, v in cpp_circuit)
    print(f"   Total Cost: {cpp_total_cost}")

    # Shortest Path (A*) result
    print("\n3. Shortest Path from Node 1 to last Node (using A*):")
    print(f"   Path: {shortest_path}")
    print(f"   Total Cost: {sum(G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))}")

# Call functions to display results and visualize the graph
display_results(tsp_path, cpp_circuit, shortest_path)
