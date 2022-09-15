from Diffraction import Diffraction

if __name__ == '__main__':
    t=1
    while t == 1:
        slab = Diffraction()
        slab.welcome_and_get_type()
        slab.m = slab.get_moment()
        slab.l = slab.get_length()

        slab.analize_results()

        x = input("Sprawdzic ugiecie dla kolejnej plyty? T/N\t")
        if x == "T" or x == "t": continue
        else: t=0




