import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi, type User, type CreateUserRequest, type LoginRequest } from '../api/user';
import { queryKeys } from '../lib/query-client';
import { message } from 'antd';

/**
 * 사용자 목록 조회 훅
 */
export const useUsers = () => {
    return useQuery({
        queryKey: queryKeys.users.lists(),
        queryFn: userApi.getUsers,
        // select: (users: User[]) => users.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()),
    });
};

/**
 * 특정 사용자 조회 훅
 */
export const useUser = (id: number) => {
    return useQuery({
        queryKey: queryKeys.users.detail(id),
        queryFn: () => userApi.getUser(id),
        enabled: !!id,
    });
};

/**
 * 현재 사용자 정보 조회 훅
 */
export const useCurrentUser = () => {
    return useQuery({
        queryKey: queryKeys.auth.currentUser(),
        queryFn: userApi.getCurrentUser,
        // 토큰이 있을 때만 요청
        enabled: !!localStorage.getItem('access_token'),
    });
};

/**
 * 사용자 생성 뮤테이션 훅
 */
export const useCreateUser = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (userData: CreateUserRequest) => userApi.createUser(userData),
        onSuccess: (newUser: User) => {
            // 사용자 목록 쿼리 무효화 (자동 리페치)
            queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });

            // 새 사용자를 캐시에 직접 추가 (Optimistic Update)
            queryClient.setQueryData(queryKeys.users.detail(newUser.id), newUser);

            message.success('회원가입이 완료되었습니다.');
        },
        onError: (error: any) => {
            console.error('사용자 생성 실패:', error);

            // 서버에서 보낸 상세 에러 메시지 표시
            const errorMessage = error?.response?.data?.detail || '회원가입에 실패했습니다.';
            message.error(errorMessage);
        },
    });
};

/**
 * 사용자 탈퇴 뮤테이션 훅
 */
export const useDeleteUser = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id }: { id: number; }) =>
            userApi.deleteUser(id),
        onSuccess: (deletedUser: User) => {
            // 해당 사용자 탈퇴 처리 후 상세 정보 업데이트
            queryClient.setQueryData(queryKeys.users.detail(deletedUser.id), deletedUser);

            // 사용자 목록도 업데이트
            queryClient.invalidateQueries({ queryKey: queryKeys.users.lists() });

            message.success('탈퇴되었습니다.');
        },
        onError: (error: any) => {
            console.error('사용자 탈퇴 실패:', error);

            // 서버에서 보낸 상세 에러 메시지 표시
            const errorMessage = error?.response?.data?.detail || '사용자 탈퇴에 실패했습니다.';
            message.error(errorMessage);
        },
    });
};

/**
 * 로그인 뮤테이션 훅
 */
export const useLogin = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (credentials: LoginRequest) => userApi.login(credentials),
        onSuccess: (response) => {
            // 토큰 저장
            localStorage.setItem('access_token', response.access_token);

            // 현재 사용자 정보 캐시에 저장
            queryClient.setQueryData(queryKeys.auth.currentUser(), response.user);

            message.success('로그인 성공!');
        },
        onError: (error: any) => {
            console.error('로그인 실패:', error);

            // 서버에서 보낸 상세 에러 메시지 표시
            const errorMessage = error?.response?.data?.detail || '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.';
            message.error(errorMessage);
        },
    });
};

/**
 * 로그아웃 함수
 */
export const useLogout = () => {
    const queryClient = useQueryClient();

    return () => {
        // 토큰 제거
        localStorage.removeItem('access_token');

        // 모든 쿼리 캐시 클리어
        queryClient.clear();

        message.success('로그아웃되었습니다.');
    };
};
