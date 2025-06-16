import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card } from '../common/Card';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';

export const SignalCard = ({ signal }) => {
  const isLong = signal?.type === 'LONG';

  return (
    <Card>
      <View style={styles.header}>
        <Text style={styles.symbol}>{signal?.symbol}</Text>
        <Text style={[
          styles.type,
          { color: isLong ? colors.success : colors.error }
        ]}>
          {signal?.type}
        </Text>
      </View>
      
      <View style={styles.priceContainer}>
        <View>
          <Text style={styles.label}>Entry Price</Text>
          <Text style={styles.price}>{signal?.entry_price}</Text>
        </View>
        <View>
          <Text style={styles.label}>Target Price</Text>
          <Text style={styles.price}>{signal?.target_price}</Text>
        </View>
      </View>

      <View style={styles.footer}>
        <Text style={styles.quality}>{signal?.signal_class}</Text>
        <Text style={styles.timeframe}>{signal?.trend_timeframe}</Text>
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  symbol: {
    fontSize: typography.sizes.h3,
    fontWeight: typography.weights.bold,
    color: colors.white,
  },
  type: {
    fontSize: typography.sizes.body,
    fontWeight: typography.weights.medium,
  },
  priceContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  label: {
    fontSize: typography.sizes.small,
    color: colors.lightGray,
    marginBottom: 4,
  },
  price: {
    fontSize: typography.sizes.body,
    color: colors.white,
    fontWeight: typography.weights.medium,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  quality: {
    fontSize: typography.sizes.small,
    color: colors.highlight,
  },
  timeframe: {
    fontSize: typography.sizes.small,
    color: colors.lightAccent,
  }
});