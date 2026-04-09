import React from 'react';

const SideNavBar = () => {
  return (
    <aside className='fixed md:relative flex flex-col h-full w-72 py-8 pl-6 bg-slate-100 dark:bg-slate-900 z-40 transition-all duration-300 ease-in-out'>
      <div className='mb-10 pr-6'>
        <div className='flex items-center gap-3 mb-6'>
          <div className='w-10 h-10 rounded-full bg-surface-container-highest flex items-center justify-center overflow-hidden'>
            <img alt='User Profile' className='w-full h-full object-cover' src='https://lh3.googleusercontent.com/aida-public/AB6AXuB3dmt9_laypBHLPGK5NURhJ_SArt_FrTBklYAWlDJQ6OMH5xXU1HaYUBQtHo2bE6StnPAmg6g_-UTUXhA8SAsgCpnZaJr1Ge8EV_Pya1j-ieEkRpv8bRuzr7Xh1q5dk_wSUoyEI1DFQ0hjJkxie40o8UNwHkDByciM-903fcz7lDPvpDemJGhRu54SHK2foCtU5elhtiPIbLwUBJ4Dzw7OeuMLui_bO6nQJwrhz_tqiaG28rJUAoOqfEkSPw5-DY4VZbRR6LoK-f0'/>
          </div>
          <div>
            <div className='text-blue-950 font-inter text-sm font-semibold'>Corporate Account</div>
            <div className='text-slate-500 text-xs'>Premium Tier</div>
          </div>
        </div>
        <button className='w-full bg-primary text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2 scale-98-active-transition'>
          <span className='material-symbols-outlined text-lg'>add</span>
          New Quote
        </button>
      </div>
      <nav className='flex flex-col gap-2 font-inter text-sm font-semibold'>
        <a className='bg-white dark:bg-slate-800 text-blue-900 dark:text-emerald-400 rounded-l-xl shadow-sm py-3 px-4 flex items-center gap-3 transition-all' href='#'>
          <span className='material-symbols-outlined'>calculate</span>
          Calculator
        </a>
        <a className='text-slate-600 dark:text-slate-400 py-3 px-4 flex items-center gap-3 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-l-xl transition-all' href='#'>
          <span className='material-symbols-outlined'>description</span>
          Saved Quotes
        </a>
        <a className='text-slate-600 dark:text-slate-400 py-3 px-4 flex items-center gap-3 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-l-xl transition-all' href='#'>
          <span className='material-symbols-outlined'>verified_user</span>
          Active Policies
        </a>
        <a className='text-slate-600 dark:text-slate-400 py-3 px-4 flex items-center gap-3 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-l-xl transition-all' href='#'>
          <span className='material-symbols-outlined'>folder_shared</span>
          Document Vault
        </a>
        <div className='mt-auto pt-4 border-t border-slate-200/50 dark:border-slate-800 pr-6'>
          <a className='text-slate-600 dark:text-slate-400 py-3 px-4 flex items-center gap-3 hover:bg-white/50 dark:hover:bg-slate-800/50 rounded-l-xl transition-all' href='#'>
            <span className='material-symbols-outlined'>settings</span>
            Settings
          </a>
        </div>
      </nav>
    </aside>
  );
};

export default SideNavBar;