import React from 'react';

const Header = () => {
  return (
    <header className='bg-slate-50 dark:bg-slate-950 flex justify-between items-center w-full px-12 h-20 max-w-[1920px] mx-auto z-50'>
      <div className='text-xl font-bold tracking-tighter text-blue-950 dark:text-white font-headline'>ShieldArchitect</div>
      <nav className='hidden md:flex items-center gap-8 font-manrope text-sm font-medium tracking-tight'>
        <a className='text-slate-500 hover:text-blue-900 transition-colors duration-200' href='#'>Policies</a>
        <a className='text-slate-500 hover:text-blue-900 transition-colors duration-200' href='#'>Claims</a>
        <a className='text-slate-500 hover:text-blue-900 transition-colors duration-200' href='#'>Renewals</a>
        <a className='text-slate-500 hover:text-blue-900 transition-colors duration-200' href='#'>Support</a>
      </nav>
      <div className='flex items-center gap-6'>
        <button className='bg-primary text-on-primary px-5 py-2.5 rounded-lg text-sm font-semibold transition-colors duration-200 hover:bg-primary-container scale-98-active-transition'>Agent Portal</button>
        <div className='flex items-center gap-4 text-slate-500'>
          <span className='material-symbols-outlined cursor-pointer hover:text-blue-900'>notifications</span>
          <span className='material-symbols-outlined cursor-pointer hover:text-blue-900'>account_circle</span>
        </div>
      </div>
    </header>
  );
};

export default Header;