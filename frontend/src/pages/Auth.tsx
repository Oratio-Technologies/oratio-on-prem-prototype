// Auth.tsx
import { useState } from 'react';
import { supabase } from '../lib/supabase';
import { useNavigate } from 'react-router-dom';
import type { AuthError } from '@supabase/supabase-js';
import Oratio from '../assets/Oratio.png';

export default function Auth() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const validateInputs = () => {
    let isValid = true;

    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Please enter a valid email address.');
      isValid = false;
    } else {
      setEmailError('');
    }

    if (!password || password.length < 6) {
      setPasswordError('Password must be at least 6 characters long.');
      isValid = false;
    } else {
      setPasswordError('');
    }

    return isValid;
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateInputs()) return;

    try {
      setLoading(true);
      const { error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;
      alert('Check your email for the confirmation link!');
    } catch (error) {
      const authError = error as AuthError;
      alert(authError.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateInputs()) return;

    try {
      setLoading(true);
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw error;
      navigate('/');
    } catch (error) {
      const authError = error as AuthError;
      alert(authError.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      setLoading(true);
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo: `${window.location.origin}/` },
      });
      if (error) throw error;
    } catch (error) {
      const authError = error as AuthError;
      alert(authError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center dark:bg-eerie-black bg-white">
      <div className="w-full max-w-md p-8 rounded-lg shadow-md dark:bg-green-3000 bg-white border dark:border-green">
        <div className="text-center mb-6">
          <div className="flex justify-center items-center gap-3">
            <h2 className="text-3xl font-bold dark:text-white text-black">
              Welcome to Oratio
            </h2>
            <img src={Oratio} alt="Oratio Logo" className="w-10 h-10" />
          </div>
          <p className="mt-2 text-sm dark:text-gray-400 text-gray-700">
            Sign in to start your conversation
          </p>
        </div>

        <form className="space-y-6" onSubmit={handleSignIn}>
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium dark:text-white text-black"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 rounded-md shadow-sm dark:bg-green-3000 dark:text-white dark:border-green-1500 border border-gray-300 focus:outline-none focus:ring "
              placeholder="your@email.com"
            />
            {emailError && (
              <p className="mt-1 text-sm text-red-500">{emailError}</p>
            )}
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium dark:text-white text-black"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 rounded-md shadow-sm dark:bg-green-3000 dark:text-white dark:border-green-1500 border border-gray-300 focus:outline-none focus:ring "
              placeholder="••••••"
            />
            {passwordError && (
              <p className="mt-1 text-sm text-red-500">{passwordError}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full border border-gray-300 py-2 px-4 rounded-md text-sm font-medium dark:bg-green-3000 dark:text-white text-black hover:opacity-90 focus:outline-none focus:ring-2 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Sign In'}
          </button>

          <button
            type="button"
            onClick={handleSignUp}
            disabled={loading}
            className="w-full py-2 px-4 rounded-md  border border-gray-300 text-sm font-medium dark:bg-green-3000 dark:text-white text-black hover:opacity-90 focus:outline-none focus:ring-2  disabled:opacity-50"
          >
            Create Account
          </button>
        </form>

        <div className="mt-6 relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t dark:border-gray-600"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white dark:bg-green-3000 text-gray-500 dark:text-gray-400">
              or
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="mt-6 w-full border border-gray-300 flex items-center justify-center gap-3 py-2 px-4 rounded-md text-sm font-medium dark:bg-green-3000 dark:text-white text-black hover:opacity-90 focus:outline-none focus:ring-2 disabled:opacity-50"
        >
          <img src="/google.svg" alt="Google logo" className="w-5 h-5" />
          {loading ? 'Processing...' : 'Continue with Google'}
        </button>
      </div>
    </div>
  );
}
