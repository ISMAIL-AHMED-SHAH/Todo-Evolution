'use client';

import { UserProvider } from '../contexts/UserContext';
import { ReactNode } from 'react';

interface UserProviderWrapperProps {
  children: ReactNode;
}

export default function UserProviderWrapper({ children }: UserProviderWrapperProps) {
  return <UserProvider>{children}</UserProvider>;
}