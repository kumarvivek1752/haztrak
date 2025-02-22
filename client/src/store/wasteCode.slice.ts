import { createApi } from '@reduxjs/toolkit/query/react';
import { htApiBaseQuery } from 'store/baseQuery';
import { Code } from 'types/wasteLine';

/**
 * A RTK Query Api for fetching codes.
 * the createApi function takes autmatically generates react hooks,
 */
export const wasteCodeApi = createApi({
  reducerPath: 'wasteCodeApi',
  baseQuery: htApiBaseQuery({
    baseUrl: `${process.env.REACT_APP_HT_API_URL}/api/trak/code/`,
  }),
  endpoints: (build) => ({
    getWasteCodes: build.query<Array<Code>, string>({
      query: (type) => ({ url: `waste/${type}`, method: 'get' }),
    }),
  }),
});

export const { useGetWasteCodesQuery } = wasteCodeApi;
