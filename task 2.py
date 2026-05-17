import matplotlib.pyplot as plt
import matplotlib.patches as patches
from constraint import Problem

constituencies = [
    'Westlands', 'Dagoretti North', 'Dagoretti South', "Lang'ata", 'Kibra',
    'Roysambu', 'Kasarani', 'Ruaraka', 'Embakasi South', 'Embakasi North',
    'Embakasi Central', 'Embakasi East', 'Embakasi West', 'Makadara', 'Kamukunji',
    'Starehe', 'Mathare'
]

neighbours = {
    'Westlands':       ['Dagoretti North', 'Kasarani', 'Starehe'],       
    'Dagoretti North': ['Westlands', 'Dagoretti South', 'Kibra'],
    'Dagoretti South': ['Dagoretti North', "Lang'ata", 'Kibra'],
    "Lang'ata":        ['Dagoretti South', 'Kibra'],
    'Kibra':           ['Dagoretti North', 'Dagoretti South', "Lang'ata", 'Makadara'],
    'Roysambu':        ['Kasarani', 'Ruaraka'],                            
    'Kasarani':        ['Roysambu', 'Ruaraka', 'Westlands', 'Mathare'],
    'Ruaraka':         ['Roysambu', 'Kasarani', 'Embakasi North', 'Mathare'],
    'Embakasi South':  ['Embakasi North', 'Embakasi East'],
    'Embakasi North':  ['Ruaraka', 'Embakasi South', 'Embakasi East', 'Embakasi Central'],
    'Embakasi Central':['Embakasi North', 'Embakasi East', 'Embakasi West'],
    'Embakasi East':   ['Embakasi South', 'Embakasi North', 'Embakasi Central', 'Embakasi West'],
    'Embakasi West':   ['Embakasi Central', 'Embakasi East', 'Makadara'],
    'Makadara':        ['Kibra', 'Embakasi West', 'Kamukunji', 'Starehe'],
    'Kamukunji':       ['Makadara', 'Starehe'],
    'Starehe':         ['Westlands', 'Makadara', 'Kamukunji', 'Mathare'], 
    'Mathare':         ['Kasarani', 'Ruaraka', 'Starehe']                  
}

colours_used = ['Red', 'Green', 'Blue', 'Yellow']

problem = Problem()
problem.addVariables(constituencies, colours_used)

added = set()
for region in constituencies:
    for neighbor in neighbours[region]:
        pair = tuple(sorted([region, neighbor]))
        if pair not in added:
            problem.addConstraint(lambda x, y: x != y, (region, neighbor))
            added.add(pair)

solution = problem.getSolution()
if solution is None:
    print("Error: No solution found!")
    exit()

pos = {
    'Westlands':        (-1.8,  0.8),
    'Dagoretti North':  (-0.9,  0.8),
    'Dagoretti South':  (-0.9,  0.0),
    "Lang'ata":         (-0.9, -0.7),
    'Kibra':            (-1.8, -0.2),
    'Roysambu':         ( 0.1,  1.0),
    'Kasarani':         ( 0.9,  1.0),
    'Ruaraka':          ( 1.7,  0.6),
    'Embakasi South':   ( 1.7, -0.7),
    'Embakasi North':   ( 1.7,  0.0),
    'Embakasi Central': ( 0.1, -0.3),
    'Embakasi East':    ( 0.1, -0.9),
    'Embakasi West':    ( 0.9, -0.6),
    'Makadara':         ( 0.9,  0.0),
    'Kamukunji':        ( 0.9, -1.1),
    'Starehe':          ( 0.1,  0.4),
    'Mathare':          ( 0.1,  1.0),
}

# Small uniform tiles to prevent ovelapping 
tile_w, tile_h = 0.75, 0.55
rects = {r: [pos[r][0] - tile_w/2, pos[r][1] - tile_h/2, tile_w, tile_h]
         for r in constituencies}

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.5, 1.5)
oval = patches.Ellipse((0, 0), 4.5, 2.8, color='none')
ax.add_patch(oval)

for reg in constituencies:
    r = rects[reg]
    patch = patches.Rectangle(
        (r[0], r[1]), r[2], r[3],
        facecolor=solution[reg],         
        edgecolor='white', linewidth=1.5,
        clip_path=oval, clip_on=True
    )
    ax.add_patch(patch)
    ax.text(pos[reg][0], pos[reg][1], reg, color='white',
            weight='bold', fontsize=7, ha='center', va='center')

plt.title("CSP: Nairobi Constituencies Map Colouring", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()