import React from 'react';
import VehicleDetailsForm from './VehicleDetailsForm';
import EstimatedPremiumDisplay from './EstimatedPremiumDisplay';

const MainContent = () => {
  return (
    <main className='flex-1 overflow-y-auto px-12 py-10 flex flex-col gap-8 max-w-[1648px]'>
      <section className='flex flex-col md:flex-row gap-12 h-full'>
        <VehicleDetailsForm />
        <EstimatedPremiumDisplay />
      </section>
    </main>
  );
};

export default MainContent;