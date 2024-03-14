## Notes:

If I use `self.image`, it will keep flipping, and I think it's because whenever we perform draw, we change the original `self.image` so it flips again.
On the other hand, it we assign `img`, we don't have the problem and I guess it's because that it get set as a new variable, so the code

```
pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
```

only get run once.

```
    def draw(self, surface):
        self.image = pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
        print('img after', img)
        surface.blit(self.image, (self.rect.x-self.offset[0], self.rect.y- self.offset[1])) #source, dest
```

```
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False) # surface, flip_x, flip_y
        print('img after', img)
        surface.blit(img, (self.rect.x-self.offset[0], self.rect.y- self.offset[1])) #source, dest
```
