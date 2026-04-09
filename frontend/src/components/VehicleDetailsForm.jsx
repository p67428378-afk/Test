import React, { useState } from 'react';
import axios from 'axios';

const VehicleDetailsForm = () => {
  const [formData, setFormData] = useState({
    vehicleMake: '',
    vehicleModel: '',
    vehicleYear: '',
    ncbTier: 'Tier 1',
  });

  const [premium, setPremium] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/v1/insurance/premium/calculate', {
        baseRate: 500,
        ncbTier: formData.ncbTier,
        vehicleMultiplier: 1.2, // This should be dynamic based on vehicle details
      });
      setPremium(response.data.premium);
    } catch (error) {
      console.error('Error calculating premium:', error);
    }
  };

  return (
    <div className='flex-grow max-w-2xl bg-surface-container-low rounded-xl p-10 flex flex-col'>
      <h1 className='font-headline text-3xl font-bold tracking-tight text-primary mb-2'>Vehicle Details</h1>
      <p className='text-on-surface-variant mb-10'>Provide the technical specifications of your vehicle to generate an accurate architectural quote.</p>
      <form className='space-y-8 flex-grow' onSubmit={handleSubmit}>
        <div className='grid grid-cols-1 md:grid-cols-2 gap-8'>
          <div className='space-y-2'>
            <label className='block font-label text-xs font-semibold text-on-surface-variant tracking-wider uppercase'>Vehicle Make</label>
            <input className='w-full bg-surface-container-highest border-0 rounded p-4 text-on-surface focus:ring-2 focus:ring-primary focus:bg-surface-container-lowest transition-all' placeholder='e.g. Mercedes-Benz' type='text' name='vehicleMake' value={formData.vehicleMake} onChange={handleChange} />
          </div>
          <div className='space-y-2'>
            <label className='block font-label text-xs font-semibold text-on-surface-variant tracking-wider uppercase'>Vehicle Model</label>
            <input className='w-full bg-surface-container-highest border-0 rounded p-4 text-on-surface focus:ring-2 focus:ring-primary focus:bg-surface-container-lowest transition-all' placeholder='e.g. S-Class Maybach' type='text' name='vehicleModel' value={formData.vehicleModel} onChange={handleChange} />
          </div>
          <div className='space-y-2'>
            <label className='block font-label text-xs font-semibold text-on-surface-variant tracking-wider uppercase'>Vehicle Year</label>
            <input className='w-full bg-surface-container-highest border-0 rounded p-4 text-on-surface focus:ring-2 focus:ring-primary focus:bg-surface-container-lowest transition-all' placeholder='2024' type='number' name='vehicleYear' value={formData.vehicleYear} onChange={handleChange} />
          </div>
          <div className='space-y-2'>
            <label className='block font-label text-xs font-semibold text-on-surface-variant tracking-wider uppercase'>NCB Tier</label>
            <select className='w-full bg-surface-container-highest border-0 rounded p-4 text-on-surface focus:ring-2 focus:ring-primary focus:bg-surface-container-lowest transition-all appearance-none' name='ncbTier' value={formData.ncbTier} onChange={handleChange}>
              <option>Tier 1</option>
              <option>Tier 2</option>
              <option>Tier 3</option>
              <option>Tier 4</option>
              <option>Tier 5</option>
            </select>
          </div>
        </div>
        <div className='pt-8'>
          <div className='bg-surface-variant/30 rounded-lg p-6 mb-8 flex items-center gap-4'>
            <span className='material-symbols-outlined text-primary'>shield</span>
            <p className='text-sm text-on-surface-variant leading-relaxed'>By calculating your premium, you agree to our structural assessment protocols and actuarial data privacy standards.</p>
          </div>
          <button className='w-full bg-primary text-on-primary py-5 rounded-lg text-lg font-bold tracking-tight hover:bg-primary-container transition-all scale-98-active-transition shadow-xl shadow-primary/10' type='submit'>
            Calculate Premium
          </button>
        </div>
      </form>
      {premium && (
        <div className="mt-8">
          <h2 className="font-headline text-2xl font-bold text-primary">Calculated Premium: ${premium}</h2>
        </div>
      )}
    </div>
  );
};

export default VehicleDetailsForm;