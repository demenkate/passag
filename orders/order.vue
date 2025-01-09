<template>
  <div class="about-page mt-3">
    <h2 class="m-2" style="color: #1d4d51; margin-bottom: 40px!important;"><strong>О нас</strong></h2>
    <div class="info-block">
      <p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
        <img class="mx-1" src="/deps/icons/time-br.svg"
             alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Режим работы:
      </p>
      <p style="margin-left: 250px; font-size: 16px; margin-bottom: 0; margin-top: -45px">
        пн-пт <strong>10:00 - 19:00</strong>
      </p>
      <p style="margin-left: 250px; font-size: 16px; margin-top: 0">
        сб-вс <strong>10:00 - 17:00</strong>
      </p>
    </div>
    <div class="info-block">
      <p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
        <img class="mx-1" src="/deps/icons/phone-br.svg"
             alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Телефон:
        <span style="margin-left: 70px; font-size: 16px; margin-bottom: 0">+7 (950) 700-66-48</span>
      </p>
    </div>
    <div class="info-block">
      <p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
        <img class="mx-1" src="/deps/icons/mail-br.svg"
             alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Mail:
        <span style="margin-left: 110px; font-size: 16px; margin-bottom: 0">passag@mail.ru</span>
      </p>
    </div>
    <div class="info-block">
      <p style="font-size: 18px; margin-bottom: 10px; margin-left: 50px">
        <img class="mx-1" src="/deps/icons/adres-br.svg"
             alt="Catalog Icon" width="32" height="32" style="margin-bottom: 10px"> Адрес:
        <span style="margin-left: 90px; font-size: 16px; margin-bottom: 0">ул. Улица Октябрьской Революции, 23, город Смоленск</span>
      </p>
    </div>
    <iframe src="https://yandex.com/map-widget/v1/?um=constructor%3Aec8f4363eaa5434b6052a4e24b1f8aacc07b98c982486aa1e07b67ca74afc9e3&amp;source=constructor"
            width="400" height="300" style="margin-left: 250px"></iframe>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-page {
  margin-top: 3rem;
}
.info-block {
  margin-bottom: 10px;
}
.mx-1 {
  margin-left: 0.25rem;
  margin-right: 0.25rem;
}
</style>