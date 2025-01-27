

def recalculate(ingredients,eatvalues,oldportion,newportion):
    if oldportion<=0 or newportion<=0:
        raise ValueError("Wielkość porcji musi być dodatnia")

    multiplier=newportion/oldportion
    newAmounts=[]
    for ingr in ingredients:
        amount=ingr.ilosc*multiplier
        if amount<ingr.jednostka.minimalnaWartosc:
            raise ValueError(f"Nie można przeliczyc {ingr.nazwaSkladnika}")
        else:
            amount=round(amount/ingr.jednostka.minimalnaWartosc)*ingr.jednostka.minimalnaWartosc
        newAmounts.append(amount)
    
    i=0
    for ingr in ingredients:
        ingr.ilosc=newAmounts[i]
        i+=1

    for k in eatvalues:
        eatvalues[k]*=multiplier
        eatvalues[k]=round(eatvalues[k],1)