#!/usr/bin/env python
import cairo
import random


SIZE = 32
MAX_WIDTH = 3
MAX_CURVES = 3
MAX_TRANS = 4


def random_color():
    return random.random(), random.random(), random.random()


def get_left_half_point(ctx):
    "Get a point in the left half of the surface"
    surf = ctx.get_group_target()
    maxw = surf.get_width()/2
    maxh = surf.get_height()
    return random.randint(0, maxw), random.randint(0, maxh)


def get_point(ctx):
    "Get a point in the on the surface"
    surf = ctx.get_group_target()
    maxw = surf.get_width()
    maxh = surf.get_height()
    return random.randint(0, maxw), random.randint(0, maxh)


def get_right_reflection(ctx, point):

    w = ctx.get_group_target().get_width()
    return w - point[0], point[1]


def draw_symmetric_curve(ctx):

    ctx.set_source_rgb(*random_color())
    start, p1, p2, end = map(get_left_half_point, [ctx]*4)

    ctx.set_line_width(random.randint(1, MAX_WIDTH))
    ctx.move_to(*start)
    ctx.curve_to(*(p1 + p2 + end))
    ctx.stroke()

    f = lambda p: get_right_reflection(ctx, p)
    start, p1, p2, end = map(f, [start, p1, p2, end])

    ctx.move_to(*start)
    ctx.curve_to(*(p1 + p2 + end))
    ctx.stroke()


def draw_nonsymmetric_curve(ctx):

    start, p1, p2, end = map(get_point, [ctx]*4)

    ctx.set_source_rgb(*random_color())
    ctx.set_line_width(random.randint(1, MAX_WIDTH))
    ctx.move_to(*start)
    ctx.curve_to(*(p1 + p2 + end))
    ctx.stroke()


def genereate_symmetric_image(filename):

    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, SIZE, SIZE)
    ctx = cairo.Context(surf)

    ctx.set_source_rgb(*random_color())
    ctx.paint()

    x = random.randint(0, MAX_TRANS)
    y = random.randint(0, MAX_TRANS)
    ctx.translate(x, y)
    #ctx.rotate(-PI/2 + random.random()*PI)

    num_curves = random.randint(1, MAX_CURVES)
    for i in range(num_curves):
        draw_symmetric_curve(ctx)

    surf.write_to_png(filename)
    surf.finish()


def genereate_nonsymmetric_image(filename):

    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, SIZE, SIZE)
    ctx = cairo.Context(surf)

    ctx.set_source_rgb(*random_color())
    ctx.paint()

    x = random.randint(0, MAX_TRANS)
    y = random.randint(0, MAX_TRANS)
    ctx.translate(x, y)
    #ctx.rotate(-PI/2 + random.random()*PI)

    num_curves = random.randint(1, MAX_CURVES)
    for i in range(num_curves):
        draw_nonsymmetric_curve(ctx)

    surf.write_to_png(filename)
    surf.finish()

for i in range(10000):
    filename = 'samples/symmetric/%3d.png' % i
    genereate_symmetric_image(filename)


for i in range(10000):
    filename = 'samples/nonsymmetric/%3d.png' % i
    genereate_nonsymmetric_image(filename)
