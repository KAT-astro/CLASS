import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
from classy import Class

# --- 計算と描画を行うメイン関数 ---
def update_cmb(h, omega_b, omega_cdm, n_s, A_s_1e9):
    # A_s を 10^9 倍から戻す
    A_s = A_s_1e9 * 1e-9
    
    # CLASSの設定
    # CMBを計算するときは 'output': 'tCl,pCl,lCl' を指定し
    # レンズ効果 ('lensing': 'yes') を入れるのが標準的です
    params = {
        'output': 'tCl, pCl, lCl',
        'lensing': 'yes',
        'h': h,
        'omega_b': omega_b,
        'omega_cdm': omega_cdm,
        'n_s': n_s,
        'A_s': A_s
    }
    
    cosmo = Class()
    try:
        cosmo.set(params)
        cosmo.compute()

        # C_lを取得 (l=2500まで)
        cls = cosmo.lensed_cl(2500)
        l = cls['ell'][2:]          # l=0, 1 は除外
        cl_tt = cls['tt'][2:]
        
        # D_l = l(l+1)C_l / 2pi に変換。
        # 1e12 を掛けて単位を [micro K^2] に調整
        dl_tt = l * (l + 1) * cl_tt / (2 * np.pi) * 1e12
        
        plt.figure(figsize=(10, 6))
        plt.plot(l, dl_tt, lw=2, color='firebrick')
        
        # 見栄えの設定
        plt.xlabel(r'Multipole moment $\ell$', fontsize=14)
        plt.ylabel(r'$\ell(\ell+1)C_\ell^{TT} / 2\pi \ [\mu\mathrm{K}^2]$', fontsize=14)
        plt.title('Interactive CMB Power Spectrum', fontsize=16)
        plt.grid(True, alpha=0.3)
        
        # 変化がわかりやすいように軸を固定
        plt.xlim(2, 2500)
        plt.ylim(0, 6000) 
        
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # メモリ解放
        cosmo.struct_cleanup()
        cosmo.empty()

# --- スライダー UI の作成 ---
style = {'description_width': '150px'}
layout = widgets.Layout(width='600px')

# continuous_update=False でマウスを離した時に再描画
s_h = widgets.FloatSlider(value=0.67, min=0.5, max=0.9, step=0.01, description='h (Hubble)', **{'style':style, 'layout':layout, 'continuous_update':False})
s_ob = widgets.FloatSlider(value=0.022, min=0.015, max=0.035, step=0.001, description='omega_b (Baryons)', **{'style':style, 'layout':layout, 'continuous_update':False})
s_oc = widgets.FloatSlider(value=0.12, min=0.05, max=0.25, step=0.01, description='omega_cdm (CDM)', **{'style':style, 'layout':layout, 'continuous_update':False})
s_ns = widgets.FloatSlider(value=0.96, min=0.8, max=1.2, step=0.01, description='n_s (Spectral Index)', **{'style':style, 'layout':layout, 'continuous_update':False})
s_as = widgets.FloatSlider(value=2.1, min=1.0, max=4.0, step=0.1, description='10^9 * A_s (Amplitude)', **{'style':style, 'layout':layout, 'continuous_update':False})

# UIの表示
ui = widgets.VBox([s_h, s_ob, s_oc, s_ns, s_as])
out = widgets.interactive_output(update_cmb, {'h': s_h, 'omega_b': s_ob, 'omega_cdm': s_oc, 'n_s': s_ns, 'A_s_1e9': s_as})

display(ui, out)