/**
 * Откладывает выполнение функции при каждом повторном вызове в течение указанного промежута времени
 * И запускает ее лишь один раз в конце,
 * @param {Function} callback Исходная функция.
 * @param {number} threshold Период, в течение которого повторные вызовы будут 
 * @returns  {Function}
 */
export default function debounce(callback, threshold) {
   // По умолчанию даем задержку в полсекунды.
   if (typeof threshold !== 'number') {
      threshold = 500;
   }

   let timerId = null;

   return function() {
      // Теперь вызывают наш декоратор вместо исходной функции.
      // А значит все аргументы приходят сюда.
      const callbackArgs = arguments;

      // У функции после декорирования могли поменять контекст.
      const context = this;

      // Если вызвали функцию повторно, то сбросим текущий таймер.
      clearTimeout(timerId);

      // Запустим новый таймер.
      timerId = setTimeout(() => {
         // Вызвали исходную функцию с учетом аргументов.
         callback.apply(context, callbackArgs);

         // Сбросили таймер.
         timerId = null;
      }, threshold);
   }
};
