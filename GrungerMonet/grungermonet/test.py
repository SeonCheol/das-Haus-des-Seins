import grungermonet

if '__main__' == __name__:
    grunger = grungermonet.GrungerMonet()
    print grunger.dist_per_index
    print grunger.sound_speed

    grunger.play()