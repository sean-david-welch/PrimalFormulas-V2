import config from '../lib/env';
import resources from '../lib/resources';

import { useMutation, useQueries, useQuery, useQueryClient } from '@tanstack/react-query';
import { Resources } from '../types/dataTypes';

export const useGetResource = <T>(resourceKey: keyof Resources) => {
	const { endpoint, queryKey } = resources[resourceKey];

	const resource = useQuery<T, Error>({
		queryKey: [queryKey],
		queryFn: async () => {
			const response = await fetch(endpoint, { credentials: 'include' });

			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		},
	});

	return resource;
};

export const useGetResourceById = <T>(resourceKey: keyof Resources, id: string) => {
	const { endpoint, queryKey } = resources[resourceKey];

	const url = `${endpoint}/${id}`;

	const resource = useQuery<T, Error>({
		queryKey: [queryKey, id],
		queryFn: async () => {
			const response = await fetch(url, { credentials: 'include' });

			if (!response.ok) throw new Error('Network response was not ok');
			return response.json();
		},
	});

	return resource;
};

export const useMultipleResources = (id: string, resourceKeys: (keyof Resources)[]) => {
	const queries = useQueries({
		queries: resourceKeys.map(key => ({
			queryKey: [key, id],
			queryFn: async () => {
				const resourceEntry = resources[key];
				const url = `${resourceEntry.endpoint}/${id}`;

				const response = await fetch(url);
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			},
		})),
	});

	const isLoading = queries.some(query => query.isLoading);
	const isError = queries.some(query => query.isError);
	const errors = queries.filter(query => query.error).map(query => query.error);

	const data = queries.filter(query => query.status === 'success').map(query => query.data);

	return { data, isLoading, isError, errors };
};

export const useMultipleResourcesWithoutId = (resourceKeys: (keyof Resources)[]) => {
	const queries = useQueries({
		queries: resourceKeys.map(key => ({
			queryKey: [key],
			queryFn: async () => {
				const resourceEntry = resources[key];
				const url = resourceEntry.endpoint;

				const response = await fetch(url);
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			},
		})),
	});

	const isLoading = queries.some(query => query.isLoading);
	const isError = queries.some(query => query.isError);
	const errors = queries.filter(query => query.error).map(query => query.error);

	const data = queries.filter(query => query.status === 'success').map(query => query.data);

	return { data, isLoading, isError, errors };
};

export const useMutateResource = <T>(resourceKey: keyof Resources, id?: string) => {
	const queryClient = useQueryClient();
	const { endpoint, queryKey } = resources[resourceKey];

	const buildEndpointUrl = (id?: string) => {
		return id ? `${endpoint}/${id}` : endpoint;
	};

	const mutate = useMutation({
		mutationFn: async (data: T) => {
			const url = buildEndpointUrl(id);
			const method = id ? 'PUT' : 'POST';

			const response = await fetch(url, {
				method: method,
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify(data),
			});

			if (!response.ok) {
				const errorText = await response.text();
				throw new Error(`Network response was not ok: ${response.status} ${errorText}`);
			}
			return response.json();
		},

		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: [queryKey] });
		},
	});

	return mutate;
};

export const useDeleteResource = (resourceKey: keyof Resources, id: string) => {
	const { endpoint, queryKey } = resources[resourceKey];

	const queryClient = useQueryClient();
	const url = new URL(endpoint + `/${id}`, config.baseUrl).toString();

	const mutateResouce = useMutation({
		mutationFn: async () => {
			const response = await fetch(url, {
				method: 'DELETE',
				credentials: 'include',
			});

			if (!response.ok) {
				throw new Error('network response was not ok');
			}
			return response.json();
		},

		onSuccess: () => {
			queryClient.refetchQueries({ queryKey: [queryKey] });
		},
	});

	return mutateResouce;
};
