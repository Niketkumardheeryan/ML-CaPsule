class cat:

    def __init__(self,height=42,name='harry'):
        self.name = name
        self.height=height


    def meow(self):
        print('meow')

    def change(self,height):
        self.height=height
        return height



tom=cat('tommy',72)
tom.meow()
tom.change(76)
print(tom.height)

ninja=cat()

print(ninja.name)
print(ninja.height)







