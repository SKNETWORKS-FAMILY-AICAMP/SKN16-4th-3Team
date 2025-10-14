import apiClient from './client';

// TODO: API 전달 후 타입 재정의 필요

/**
 * 사용자 관련 API 타입 정의
 */

export type GenderType = '남성' | '여성';

export interface User {
    id: number;
    nickname: string;
    username: string;
    email: string;
    created_at: string;
    gender?: GenderType;
}

export interface CreateUserRequest {
    nickname: string
    username: string;
    password: string;
    email: string;
    gender?: GenderType;
}

export interface LoginRequest {
    nickname: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user: User;
}

/**
 * 사용자 관련 API 함수들
 */
export const userApi = {
    // 모든 사용자 조회
    getUsers: async (): Promise<User[]> => {
        const response = await apiClient.get<User[]>('/users');
        return response.data;
    },

    // 특정 사용자 조회
    getUser: async (id: number): Promise<User> => {
        const response = await apiClient.get<User>(`/users/${id}`);
        return response.data;
    },

    // 사용자 생성
    createUser: async (userData: CreateUserRequest): Promise<User> => {
        const response = await apiClient.post<User>('/users', userData);
        return response.data;
    },

    // 사용자 수정 (탈퇴 시 상태 변경 용도)
    deleteUser: async (id: number): Promise<User> => {
        const response = await apiClient.put<User>(`/users/${id}`);
        return response.data;
    },

    // 로그인
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
        const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
        return response.data;
    },

    // 현재 사용자 정보 조회
    getCurrentUser: async (): Promise<User> => {
        const response = await apiClient.get<User>('/auth/me');
        return response.data;
    },
};