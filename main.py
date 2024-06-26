import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
device = 'cuda'

import argparse
import time
import torch
from data import get_data
from model import Model
from pytorchtools import EarlyStopping
from train import train_and_eval
assert(torch.cuda.is_available())

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    parser = argparse.ArgumentParser()
    parser.add_argument('-model', default = 'NRMS')
    parser.add_argument('-epochs', type = int, default = 6)
    parser.add_argument('--no_ent', action="store_true")
    parser.add_argument('-ent_emb', type = str, default = 'random')
    parser.add_argument('-times', type = int, default = 1)
    args = parser.parse_args().__dict__
    args['use_ent']  = not args['no_ent']
    del args['no_ent']
    print(args)
    for i in range(args['times']):
        train_dataset, dev_dataset, news_info, dev_users, dev_user_hist, news_ents, \
            word_emb, cate_emb, ent_emb = get_data()
        model = Model(args, word_emb, cate_emb, ent_emb).to('cuda')
        train_and_eval(model, train_dataset, dev_dataset, news_info, dev_users, dev_user_hist, news_ents, args['epochs'])
    
    
