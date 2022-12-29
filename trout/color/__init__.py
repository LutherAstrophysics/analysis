from trout.database import query

def get_color(star_number : int):
    result = query(f"SELECT color FROM color WHERE star={star_number}")
    if  len(result) == 1 and len(result[0]) == 1:
        return result[0][0]
    else:
        return None
