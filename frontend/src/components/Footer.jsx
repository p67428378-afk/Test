import React from 'react';

const Footer = () => {
  return (
    <footer className='bg-slate-50 dark:bg-slate-950 flex flex-col md:flex-row justify-between items-center px-12 py-8 w-full max-w-[1920px] mx-auto z-50'>
      <div className='font-inter text-xs tracking-wide text-slate-500 dark:text-slate-400 mb-4 md:mb-0'>
        © 2024 ShieldArchitect Insurance Services. Underwritten by Global Protection Group.
      </div>
      <div className='flex gap-8 font-inter text-xs tracking-wide'>
        <a className='text-slate-500 hover:text-blue-900 hover:underline opacity-80-hover transition-opacity' href='#'>Privacy Policy</a>
        <a className='text-slate-500 hover:text-blue-900 hover:underline opacity-80-hover transition-opacity' href='#'>Terms of Service</a>
        <a className='text-slate-500 hover:text-blue-900 hover:underline opacity-80-hover transition-opacity' href='#'>Compliance</a>
        <a className='text-slate-500 hover:text-blue-900 hover:underline opacity-80-hover transition-opacity' href='#'>Legal Disclosure</a>
      </div>
    </footer>
  );
};

export default Footer;