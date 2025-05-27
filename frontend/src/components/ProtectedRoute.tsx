// import { useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { supabase } from '../lib/supabase';

// interface ProtectedRouteProps {
//   children: React.ReactNode;
// }

// export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
//   const navigate = useNavigate();

//   useEffect(() => {
//     const checkAuth = async () => {
//       const {
//         data: { session },
//       } = await supabase.auth.getSession();
//       if (!session) {
//         navigate('/login');
//       }
//     };

//     checkAuth();

//     const {
//       data: { subscription },
//     } = supabase.auth.onAuthStateChange((_event, session) => {
//       if (!session) {
//         navigate('/login');
//       }
//     });

//     return () => {
//       subscription.unsubscribe();
//     };
//   }, [navigate]);

//   return <>{children}</>;
// };
