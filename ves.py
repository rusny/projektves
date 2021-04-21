from PIL import Image
from random import randint
import colorsys

def random_color():
  r = randint(0, 255)
  g = randint(0, 255)
  b = randint(0, 255)
  return (r, g, b)



def convert_x(width, output_width, x):
  return int(x/width * output_width)

def convert_y(height, output_height, y):
  return int(y/height * output_height)

def convert_point(width, height, output_width, output_height, X):
  return (convert_x(width, output_width, X[0]), convert_y(height, output_height, X[1]))

def hex2dec(cislo):
  vysledok = 0
  for index in range(len(cislo)):
    cifra = cislo[(index+1)*(-1)].upper()
    if ord("A") <= ord(cifra) <= ord("F"):
      cifra = ord(cifra) - 65 + 10
    else:
      cifra = int(cifra)

    vysledok += cifra * 16 ** index
  return vysledok

      
def hexColor(color):
  r = hex2dec(color[1:3])
  g = hex2dec(color[3:5])
  b = hex2dec(color[5:7])
  return (r, g, b)


def linePixels(ax, ay, bx, by):
  pixels = []
  if ax == bx:
    if ay > by:
        ax,ay,bx,by=bx,by,ax,ay
    for y in range(ay, by + 1):
      pixels.append((ax, y))
  elif ay == by:
    if ax > bx:
        ax,ay,bx,by=bx,by,ax,ay
    for x in range(ax, bx + 1):
      pixels.append((x, ay))
  else:
    if ax > bx:
        ax,ay,bx,by=bx,by,ax,ay
    dx = bx - ax
    dy = by - ay
    if abs(dy/dx) > 1:
      for y in range(min(ay, by), max(ay, by) + 1):
        x = int((y - ay + (dy/dx) * ax) * (dx/dy))
        pixels.append((x, y))
    else:
      for x in range(min(ax, bx), max(ax, bx) + 1):
        y = int((by - ay)/(bx - ax) * (x - ax) + ay)
        pixels.append((x, y))
  return pixels

def line(im, ax, ay, bx, by, color):

  
  if ax == bx:
    if ay > by:
        ax,ay,bx,by=bx,by,ax,ay
    for y in range(ay, by + 1):
      if ax>0 and ax<im.width and y>0 and y<im.height:
        im.putpixel((ax, y), color)
  elif ay == by:
    if ax > bx:
        ax,ay,bx,by=bx,by,ax,ay
    for x in range(ax, bx + 1):
      if x>0 and x<im.width and ay>0 and ay<im.height:
        im.putpixel((x, ay), color)
  else:
    if ax > bx:
        ax,ay,bx,by=bx,by,ax,ay
    dx = bx - ax
    dy = by - ay
    if abs(dy/dx) > 1:
      for y in range(min(ay, by), max(ay, by) + 1):
        x = int((y - ay + (dy/dx) * ax) * (dx/dy))
        if x>0 and x<im.width and y>0 and y<im.height:
          im.putpixel((x, y), color)
    else:
      for x in range(min(ax, bx), max(ax, bx) + 1):
        y = int((by - ay)/(bx - ax) * (x - ax) + ay)
        if x>0 and x<im.width and y>0 and y<im.height:
          im.putpixel((x, y), color)

def filled_circle(im, S, r, color):
  ''' Nakresli do obrazku im kruh so stredom v bode S a polomerom r farbou color '''
  for x in range(0, int(r/2**(1/2)) + 1):
    y = int((r**2 - x**2)**(1/2))
  
    line(im, x + S[0], y + S[1], x + S[0], -y + S[1], color)

    line(im, y + S[0], x + S[1], y + S[0], -x + S[1], color)

    line(im, -x + S[0], -y + S[1], -x + S[0], y + S[1], color)

    line(im, -y + S[0], -x + S[1], -y + S[0], x + S[1], color)

def thick_line(im, ax, ay, bx, by, thickness, color):
  ''' Nakresli do obrazku im ciaru AB s hrubkou thickness a farbou color '''

  pixels = linePixels(ax, ay, bx, by)
  for X in pixels:
    filled_circle(im, X, thickness/2, color)

def circle(im, sx, sy, r, thickness, color):
  ''' Nakresli do obrazku im kruznicu so stredom v bode S a polomerom r farbou color '''
  for x in range(0, int(r/2**(1/2)) + 1):
      
      y = int((r**2 - x**2)**(1/2))

      filled_circle(im, (x + sx, y + sy), thickness/2, color)
      filled_circle(im, (y + sx, x + sy), thickness/2, color)
      filled_circle(im, (y + sx, -x + sy), thickness/2, color)
      filled_circle(im, (x + sx, -y + sy), thickness/2, color)
      filled_circle(im, (-x + sx, -y + sy), thickness/2, color)
      filled_circle(im, (-y + sx, -x + sy), thickness/2, color)
      filled_circle(im, (-y + sx, x + sy), thickness/2, color)
      filled_circle(im, (-x + sx, y + sy), thickness/2, color)

def getY(point):
  return point[1]

def fill_triangle(im, A, B, C, color):
  V = sorted([A, B, C], key=getY)
  left = linePixels(V[0][0], V[0][1], V[1][0], V[1][1]) + linePixels(V[1][0], V[1][1], V[2][0], V[2][1])
  right = linePixels(V[0][0], V[0][1], V[2][0], V[2][1])

  Xmax = max(A[0], B[0], C[0])
  Xmin = min(A[0], B[0], C[0])

  # Ak je prostredny bod napravo, musime lavu a pravu stranu vymeniť
  if V[1][0] == Xmax:
    left, right = right, left

  for y in range(getY(V[0]), getY(V[2]) + 1):
    x1 = Xmax
    for X in left:
      if X[1] == y and X[0] < x1:
        x1 = X[0]

    x2 = Xmin
    for X in right:
      if X[1] == y and X[0] > x2:
        x2 = X[0]

    if x2 < 0:
      continue  
    if x2 > im.width:
      x2 = im.width - 1
    if x1 < 0:
      x1 = 0  

    line(im, x1, y, x2, y, color)








def render_ves(text, output_width):
  row = 0
  output_width = 600
  prikazy=text.split('\n')

  for riadok in prikazy:
    cisla = riadok.split(" ")
    prikaz = cisla[0]
    if prikaz == 'VES':
      width = int(cisla[2])
      height = int(cisla[3])
      output_height = int(height/width * output_width)
      
      obr = Image.new('RGB', (output_width, output_height), (255,255,255))

      
    elif prikaz == 'CLEAR':
      color = cisla[1]
      
      obr = Image.new('RGB', (output_width, output_height), hexColor(color))
    elif prikaz == 'LINE':
      ax = convert_x(width, output_width, int(cisla[1]))
      ay = convert_y(height, output_height, int(cisla[2]))
      bx = convert_x(width, output_width, int(cisla[3]))
      by = convert_y(height, output_height, int(cisla[4]))
      thickness = int(cisla[5])
      farba = hexColor(cisla[6])
      thick_line(obr, ax, ay, bx, by, thickness, farba)
    elif prikaz == 'RECT':
      ax = convert_x(width, output_width, int(cisla[1]))
      ay = convert_y(height, output_height, int(cisla[2]))
      rect_width = convert_x(width, output_width, int(cisla[3]))
      rect_height = convert_y(height, output_height, int(cisla[4]))
      thickness = int(cisla[5])
      farba = hexColor(cisla[6])
      thick_line(obr, ax, ay, ax+rect_width, ay, thickness, farba)
      thick_line(obr, ax+rect_width, ay, ax+rect_width, ay+rect_height, thickness, farba)
      thick_line(obr, ax, ay, ax, ay+rect_height, thickness, farba)
      thick_line(obr, ax, ay + rect_height, ax+rect_width, ay+rect_height, thickness, farba)
    elif prikaz == 'TRIANGLE':
      ax = convert_x(width, output_width, int(cisla[1]))
      ay = convert_y(height, output_height, int(cisla[2]))
      bx = convert_x(width, output_width, int(cisla[3]))
      by = convert_y(height, output_height, int(cisla[4]))
      cx = convert_x(width, output_width, int(cisla[5]))
      cy = convert_y(height, output_height, int(cisla[6]))
      thickness = int(cisla[7])
      farba = hexColor(cisla[8])
      thick_line(obr, ax, ay, bx, by, thickness, farba)
      thick_line(obr, ax, ay, cx, cy, thickness, farba)
      thick_line(obr, bx, by, cx, cy, thickness, farba)
    elif prikaz == 'CIRCLE':
      sx = convert_x(width, output_width, int(cisla[1]))
      sy = convert_y(height, output_height, int(cisla[2]))
      r = convert_x(width, output_width, int(cisla[3]))
      thickness = int(cisla[4])
      farba = hexColor(cisla[5])
      circle(obr, sx, sy, r, thickness, farba)
    elif prikaz == 'FILL_CIRCLE':
      sx = convert_x(width, output_width, int(cisla[1]))
      sy = convert_y(height, output_height, int(cisla[2]))
      r = convert_x(width, output_width, int(cisla[3]))
      farba = hexColor(cisla[4])
      filled_circle(obr, (sx,sy), r, farba)
    elif prikaz == 'FILL_TRIANGLE':
      ax = convert_x(width, output_width, int(cisla[1]))
      ay = convert_y(height, output_height, int(cisla[2]))
      bx = convert_x(width, output_width, int(cisla[3]))
      by = convert_y(height, output_height, int(cisla[4]))
      cx = convert_x(width, output_width, int(cisla[5]))
      cy = convert_y(height, output_height, int(cisla[6]))
      farba = hexColor(cisla[7])
      fill_triangle(obr, (ax, ay), (bx, by), (cx, cy), farba)
    elif prikaz == 'FILL_RECT':
      ax = convert_x(width, output_width, int(cisla[1]))
      ay = convert_y(height, output_height, int(cisla[2]))
      rect_width = convert_x(width, output_width, int(cisla[3]))
      rect_height = convert_y(height, output_height, int(cisla[4]))
      farba = hexColor(cisla[5])
      for x in range(ax, ax+rect_width+1):
        for y in range(ay, ay+rect_height+1):
          if x>0 and x<output_width and y>0 and y<output_height:
            obr.putpixel((x, y), farba)

    elif prikaz =='\n':
      continue
    elif prikaz == 'Grayscale':
      grayscale(obr)
    else:
      print(f'Syntax error on line {row+1}: Unknown command {prikaz}.')

    row += 1
  return obr


def grayscale(im):
  for x in range(im.width):
    for y in range(im.height):
      rgb = im.getpixel((x,y))
      hls = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
      bw = colorsys.hls_to_rgb(hls[0], hls[1], 0)
      im.putpixel((x,y), (int(bw[0]*255), int(bw[1]*255), int(bw[2]*255)))




