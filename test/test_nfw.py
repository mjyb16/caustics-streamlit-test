#from math import pi

#import lenstronomy.Util.param_util as param_util
import torch
from lenstronomy.LensModel.lens_model import LensModel
from utils import lens_test_helper

from caustic.cosmology import FlatLambdaCDMCosmology
from caustic.lenses import NFW

#next to imports to get Rs_angle and alpha_Rs in arcsec for lenstronomy
from lenstronomy.Cosmo.lens_cosmo import LensCosmo
from astropy.cosmology import FlatLambdaCDM

def test():
    atol = 1e-5
    rtol = 1e-5

    # Models
    lens = NFW()
    lens_model_list = ["NFW"]
    lens_ls = LensModel(lens_model_list=lens_model_list)

    # Parameters
    z_l = torch.tensor(0.5)
    z_s = torch.tensor(2.1)
    cosmology = FlatLambdaCDMCosmology()
    thx0 = torch.tensor(0.457)
    thy0 = torch.tensor(0.141)
    m = torch.tensor(1e12)
    c = torch.tensor(15.0)
    args = (z_l, z_s, cosmology, thx0, thy0, m, c)
    
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3, Ob0=0.05)
    lens_cosmo = LensCosmo(z_lens=z_l.item(), z_source=z_s.item(), cosmo=cosmo)
    Rs_angle, alpha_Rs = lens_cosmo.nfw_physical2angle(M=m.item(), c=c.item())
    
    #lenstronomy params ['Rs', 'alpha_Rs', 'center_x', 'center_y']
    kwargs_ls = [
        {
            "Rs": Rs_angle,
            "alpha_Rs": alpha_Rs,
            "center_x": thx0.item(),
            "center_y": thy0.item(),
        }
    ]

    lens_test_helper(lens, lens_ls, args, kwargs_ls, rtol, atol)
