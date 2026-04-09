import React from 'react';

const EstimatedPremiumDisplay = () => {
  return (
    <div className='w-full md:w-[420px] flex flex-col gap-6'>
      <div className='glass-panel border-0 rounded-2xl p-8 shadow-2xl shadow-blue-900/5 relative overflow-hidden flex flex-col min-h-[400px]'>
        <div className='absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16'></div>
        <div className='relative z-10'>
          <span className='inline-block px-3 py-1 bg-tertiary-fixed text-on-tertiary-fixed rounded text-[10px] font-extrabold uppercase tracking-[0.2em] mb-6'>Live Calculation</span>
          <h2 className='font-headline text-on-surface-variant text-sm font-semibold mb-2'>Estimated Annual Premium</h2>
          <div className='flex items-baseline gap-2 mb-8'>
            <span className='font-headline text-6xl font-extrabold text-primary tracking-tighter'>$2,450</span>
            <span className='font-headline text-lg font-medium text-on-surface-variant'>/yr</span>
          </div>
          <div className='space-y-6'>
            <div className='flex justify-between items-center text-sm border-b border-outline-variant/10 pb-4'>
              <span className='text-on-surface-variant'>Comprehensive Coverage</span>
              <span className='font-bold text-primary'>$1,820</span>
            </div>
            <div className='flex justify-between items-center text-sm border-b border-outline-variant/10 pb-4'>
              <span className='text-on-surface-variant'>Personal Liability</span>
              <span className='font-bold text-primary'>$430</span>
            </div>
            <div className='flex justify-between items-center text-sm border-b border-outline-variant/10 pb-4'>
              <span className='text-on-surface-variant'>Roadside Assistance</span>
              <span className='font-bold text-primary'>$200</span>
            </div>
            <div className='flex justify-between items-center text-sm pt-2'>
              <span className='text-on-surface-variant'>Monthly Payment</span>
              <span className='font-bold text-tertiary-container'>$214.50</span>
            </div>
          </div>
        </div>
        <div className='mt-auto pt-8 flex gap-3'>
          <button className='flex-1 bg-surface-container-highest text-primary py-3 rounded font-bold text-sm hover:bg-surface-variant transition-colors'>Download PDF</button>
          <button className='flex-1 bg-tertiary-container text-white py-3 rounded font-bold text-sm hover:opacity-90 transition-opacity'>Apply Now</button>
        </div>
      </div>
      <div className='bg-primary-container rounded-2xl p-8 text-white relative overflow-hidden group'>
        <div className='absolute -right-4 -bottom-4 opacity-10 group-hover:scale-110 transition-transform duration-500'>
          <span className='material-symbols-outlined text-[120px]' style={{fontVariationSettings: '\'FILL\' 1'}}>verified</span>
        </div>
        <h3 className='font-headline text-xl font-bold mb-3'>Architect Tier Benefits</h3>
        <ul className='space-y-3 text-sm text-on-primary-container'>
          <li className='flex items-center gap-2'>
            <span className='material-symbols-outlined text-tertiary-fixed text-lg'>check_circle</span>
            Zero-depreciation on all parts
          </li>
          <li className='flex items-center gap-2'>
            <span className='material-symbols-outlined text-tertiary-fixed text-lg'>check_circle</span>
            Complimentary engine protection
          </li>
          <li className='flex items-center gap-2'>
            <span className='material-symbols-outlined text-tertiary-fixed text-lg'>check_circle</span>
            24/7 Priority claims concierge
          </li>
        </ul>
      </div>
    </div>
  );
};

export default EstimatedPremiumDisplay;