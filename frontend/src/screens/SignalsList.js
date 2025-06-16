import React, { useEffect, useState } from 'react';
import { View, FlatList, StyleSheet, RefreshControl } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { SignalCard } from '../components/signals/SignalCard';
import { colors } from '../theme/colors';
import { signalsApi } from '../services/api';
import { setSignals, setLoading, setError } from '../store/slices/signalsSlice';

export const SignalsList = () => {
  const dispatch = useDispatch();
  const { signals, loading } = useSelector(state => state.signals);
  const [refreshing, setRefreshing] = useState(false);

  const fetchSignals = async () => {
    try {
      dispatch(setLoading(true));
      const response = await signalsApi.getSignals();
      dispatch(setSignals(response.data));
    } catch (error) {
      dispatch(setError(error.message));
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchSignals();
    setRefreshing(false);
  };

  useEffect(() => {
    fetchSignals();
  }, []);

  return (
    <View style={styles.container}>
      <FlatList
        data={signals}
        renderItem={({ item }) => <SignalCard signal={item} />}
        keyExtractor={item => item.symbol}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            tintColor={colors.white}
          />
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.primary,
  },
  list: {
    padding: 16,
  }
});