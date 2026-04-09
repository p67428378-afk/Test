import React from 'react';
import Header from './components/Header';
import SideNavBar from './components/SideNavBar';
import MainContent from './components/MainContent';
import Footer from './components/Footer';

function App() {
  return (
    <div className='bg-background font-body text-on-surface overflow-hidden h-screen flex flex-col'>
      <Header />
      <div className='flex flex-1 overflow-hidden'>
        <SideNavBar />
        <MainContent />
      </div>
      <Footer />
    </div>
  );
}

export default App;