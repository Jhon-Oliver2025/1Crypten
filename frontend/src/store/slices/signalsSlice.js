import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  signals: [],
  loading: false,
  error: null,
};

const signalsSlice = createSlice({
  name: 'signals',
  initialState,
  reducers: {
    setSignals: (state, action) => {
      state.signals = action.payload;
      state.loading = false;
      state.error = null;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    },
  },
});

export const { setSignals, setLoading, setError } = signalsSlice.actions;
export default signalsSlice.reducer;