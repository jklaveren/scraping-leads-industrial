function enviarEmailsMatinaisComRelatorio() {
  var aba = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var inicioLinha = 2; 
  var dados = aba.getRange(inicioLinha, 1, aba.getLastRow() - 1, 3).getValues();
  var tempoInicio = new Date().getTime();
  
  var enviadosNestaSessao = 0;
  var erros = 0;
  var seuEmail = "seu-email@gmail.com"; // <-- COLOQUE O SEU E-MAIL AQUI PARA RECEBER O RELATÓRIO

  for (var i = 0; i < dados.length; i++) {
    var nome = dados[i][0];
    var emailDestino = dados[i][1];
    var status = dados[i][2];
    
    if (status !== "Enviado" && emailDestino.includes("@")) {
      try {
        MailApp.sendEmail({
          to: emailDestino,
          subject: "Olá " + nome + ", sua mensagem matinal",
          body: "Oi " + nome + ",\n\nEspero que seu dia esteja começando bem!"
        });
        
        aba.getRange(inicioLinha + i, 3).setValue("Enviado");
        enviadosNestaSessao++;
        
        // Pausa de 1,5 segundos
        Utilities.sleep(1500); 
        
      } catch (e) {
        erros++;
        Logger.log("Erro no e-mail: " + emailDestino);
      }
    }
    
    // Verificação de tempo (limite de 5 minutos e meio)
    var tempoAtual = new Date().getTime();
    if (tempoAtual - tempoInicio > 330000) { 
      break; 
    }
  }

  // ENVIO DO RELATÓRIO PARA SI MESMO
  if (enviadosNestaSessao > 0 || erros > 0) {
    MailApp.sendEmail({
      to: seuEmail,
      subject: "Relatório de Envio Diário - Automação",
      body: "O script de envio matinal terminou.\n\n" +
            "Sucesso: " + enviadosNestaSessao + " e-mails enviados.\n" +
            "Erros: " + erros + " falhas encontradas.\n\n" +
            "Se o número de sucessos for menor que 300 e você ainda tiver e-mails pendentes, " +
            "o script parou por limite de tempo e continuará no próximo agendamento."
    });
  }
}