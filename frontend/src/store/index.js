import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import signalsReducer from './slices/signalsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    signals: signalsReducer,
  },
});