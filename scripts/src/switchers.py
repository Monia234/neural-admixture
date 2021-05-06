import custom_losses as cl
import initializations as init
import torch.nn as nn
import torch.optim as optim

class Switchers(object):
    _activations = {
        'relu': lambda x: nn.ReLU(),
        'tanh': lambda x: nn.Tanh()
    }
    _losses = {
        'mse': lambda device, frac: nn.MSELoss(reduction='mean'),
        'bce': lambda device, frac: nn.BCELoss(reduction='mean'),
        'wbce': lambda device, frac: cl.WeightedBCE(),
        'bce_mask': lambda device, frac: cl.MaskedBCE(device, mask_frac=frac),
        'mse_mask': lambda device, frac: cl.MaskedMSE(device, mask_frac=frac),
        'admixture': lambda device, frac: cl.AdmixtureLoss()
    }
    _initializations = {
        'random': lambda X, k, batch_size, seed, path: None,
        'mean_SNPs': lambda X, k, batch_size, seed, path: init.SNPsMeanInitialization.get_decoder_init(X, k),
        'mean_random': lambda X, k, batch_size, seed, path: init.RandomMeanInitialization.get_decoder_init(X, k),
        'kmeans': lambda X, k, batch_size, seed, path: init.KMeansInitialization.get_decoder_init(X, k, False, False, batch_size, seed),
        'minibatch_kmeans': lambda X, k, batch_size, seed, path: init.KMeansInitialization.get_decoder_init(X, k, True, False, batch_size, seed),
        'kmeans_logit': lambda X, k, batch_size, seed, path: init.KMeansInitialization.get_decoder_init(X, k, False, True, batch_size, seed),
        'minibatch_kmeans_logit': lambda X, k, batch_size, seed, path: init.KMeansInitialization.get_decoder_init(X, k, True, True, batch_size, seed),
        'kmeans++': lambda X, k, batch_size, seed, path: init.KMeansPlusPlusInitialization.get_decoder_init(X, k, seed),
        'binomial': lambda X, k, batch_size, seed, path: init.BinomialInitialization.get_decoder_init(X, k),
        'pca': lambda X, k, batch_size, seed, path: init.PCAInitialization.get_decoder_init(X, k),
        'admixture': lambda X, k, batch_size, seed, path: init.AdmixtureInitialization.get_decoder_init(X, k, path),
        'pckmeans': lambda X, k, batch_size, seed, path: init.PCKMeans.get_decoder_init(X, k, path)
    }
    _optimizers = {
        'adam': lambda params, lr: optim.Adam(params, lr),
        'sgd': lambda params, lr: optim.SGD(params, lr)
    }

    @classmethod
    def get_switchers(cls):
        return {
            'losses': cls._losses,
            'activations': cls._activations,
            'initializations': cls._initializations,
            'optimizers': cls._optimizers
        }
