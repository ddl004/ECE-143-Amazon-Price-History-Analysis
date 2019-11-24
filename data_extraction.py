import keepa
import numpy as np
import matplotlib as plt

def save_bestsellers_from_cat(cat, filename):
    '''Save bestsellers from given cat to numpy file
    
    :param cat: Amazon category ID
    :type cat: str
    :param filename: filename to save bestsellers to
    :type filename: str
    :return: list of bestsellers
    :rtype: list of str
    '''
    assert isinstance(cat, str)
    assert isinstance(filename, str)
    assert len(cat) > 0 and len(filename) > 0

    api_key = 'e6ihvarndmd2iee2bgeg60afm06gru9242g310tb4tv1kji72u57uon4us908d5h'
    api = keepa.Keepa(api_key)  
    # Obtain all bestsellers from category
    bestsellers = api.best_sellers_query(cat)
    np.save(filename, bestsellers)
    print("Best Sellers for Category {0} saved to {1}".format(cat, filename))

    return bestsellers

def save_products(product_ids, filename, ratings=True):
    '''Save product dicts from given ids into numpy file
    
    :param cat: product IDs
    :type cat: list of str
    :param filename: filename to save product dictionaries to
    :type filename: str
    :return: product dicts
    :rtype: list of dict
    '''
    assert isinstance(product_ids, (list, np.ndarray))
    assert all(isinstance(i, str) for i in product_ids)
    assert isinstance(filename, str)
    assert len(filename) > 0
    # Keepa API limit
    assert isinstance(ratings, bool)
    if not ratings:
        assert 0 < len(product_ids) <= 300
    else:
        # Query for ratings and reviews consumes more tokens
        assert 0 < len(product_ids) <= 150
    api_key = 'e6ihvarndmd2iee2bgeg60afm06gru9242g310tb4tv1kji72u57uon4us908d5h'
    api = keepa.Keepa(api_key)   

    try:
        # Obtain product dicts
        products = api.query(product_ids, rating=True)
        np.save(filename, products)
        print("Product Dictionaries saved to {0}".format(filename))
        return products

    # If manual exit from program due to lack of tokens
    except:
        print("Out of tokens...")
        print('Time to refill tokens: ', api.time_to_refill, '\n')
        print('Token Status: ', api.update_status())


if __name__ == "__main__":
    electronics = '172282'
    # save_bestsellers_from_cat(electronics, "bestsellers.npy")
    bestsellers = np.load("bestsellers.npy", allow_pickle=True)
    save_products(bestsellers[0:150], "product_electronics_test_ratings.npy", ratings=True)
    # products = np.load("product_electronics_300_600.npy", allow_pickle=True)
    # print(len(products))