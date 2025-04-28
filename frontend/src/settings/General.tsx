import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

import userService from '../api/services/userService';
import Dropdown from '../components/Dropdown';
import { useDarkTheme } from '../hooks';
import {
  selectChunks,
  selectPrompt,
  selectTokenLimit,
} from '../preferences/preferenceSlice';

export default function General() {
  const {
    t,
    i18n: { changeLanguage, language },
  } = useTranslation();

  // Use the translation function to get the theme labels
  const themes = [
    { label: t('settings.general.light'), value: 'light' },
    { label: t('settings.general.dark'), value: 'dark' },
  ];

  const languageOptions = [
    {
      label: 'English',
      value: 'en',
    },
    {
      label: 'German',
      value: 'de',
    },
  ];
  const chunks = ['0', '2', '4', '6', '8', '10'];
  const token_limits = new Map([
    [0, t('settings.general.none')],
    [100, t('settings.general.low')],
    [1000, t('settings.general.medium')],
    [2000, t('settings.general.default')],
    [4000, t('settings.general.high')],
    [1e9, t('settings.general.unlimited')],
  ]);
  const [prompts, setPrompts] = React.useState<
    { name: string; id: string; type: string }[]
  >([]);
  const selectedChunks = useSelector(selectChunks);
  const selectedTokenLimit = useSelector(selectTokenLimit);
  const [isDarkTheme, toggleTheme] = useDarkTheme();
  const [selectedTheme, setSelectedTheme] = React.useState(
    isDarkTheme ? themes[1] : themes[0], // Use the theme objects instead of hardcoded strings
  );
  const dispatch = useDispatch();
  const locale = localStorage.getItem('docsgpt-locale');
  const [selectedLanguage, setSelectedLanguage] = React.useState(
    locale
      ? languageOptions.find((option) => option.value === locale)
      : languageOptions[0],
  );
  const selectedPrompt = useSelector(selectPrompt);

  React.useEffect(() => {
    const handleFetchPrompts = async () => {
      try {
        const response = await userService.getPrompts();
        if (!response.ok) {
          throw new Error('Failed to fetch prompts');
        }
        const promptsData = await response.json();
        setPrompts(promptsData);
      } catch (error) {
        console.error(error);
      }
    };
    handleFetchPrompts();
  }, []);

  React.useEffect(() => {
    localStorage.setItem('docsgpt-locale', selectedLanguage?.value as string);
    changeLanguage(selectedLanguage?.value);
  }, [selectedLanguage, changeLanguage]);

  return (
    <div className="mt-12">
      <div className="mb-5">
        <p className="font-bold text-jet dark:text-bright-gray">
          {t('settings.general.selectTheme')}
        </p>
        <Dropdown
          options={themes}
          selectedValue={selectedTheme}
          onSelect={(option: { label: string; value: string }) => {
            setSelectedTheme(option);
            option.value !== selectedTheme.value && toggleTheme();
          }}
          size="w-56"
          rounded="3xl"
          border="border"
        />
      </div>
      <div className="mb-5">
        <p className="mb-2 font-bold text-jet dark:text-bright-gray">
          {t('settings.general.selectLanguage')}
        </p>
        <Dropdown
          options={languageOptions.filter(
            (languageOption) =>
              languageOption.value !== selectedLanguage?.value,
          )}
          selectedValue={selectedLanguage ?? languageOptions[0]}
          onSelect={(selectedOption: { label: string; value: string }) => {
            setSelectedLanguage(selectedOption);
          }}
          size="w-56"
          rounded="3xl"
          border="border"
        />
      </div>
    </div>
  );
}
