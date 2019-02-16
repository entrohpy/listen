import React from 'react';
import './index.scss';

const Header = ({
  children,
}) => {
  return (
    <div className="header">
    {children}
    </div>
  );
};

export default Header;
