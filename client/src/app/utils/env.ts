import { config } from 'dotenv';

config();

export const env: Record<string, string> = {
  stripeKey: process.env['STRIPE_PUBLIC_KEY'] as string,
  stripeKeyTest: process.env['TEST_PUBLIC_KEY'] as string,
};
