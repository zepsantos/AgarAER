# PIM6SD Guia de utilização
link da biblioteca: https://github.com/troglobit/pim6sd

Instalar o pim6sd através das instruções de instalação do github.

    
	git clone https://github.com/troglobit/pim6sd.git
	cd pim6sd/
	./autogen.sh
	./configure && make
	sudo make install-strip

Escolha do router RP , preferencialmente perto do servidor. Basicamente é escolhido um router para ser um RP(Rendezvous point) e para ser um Bootstrap_router ( envia mensagens de bootstrap para os outros pim routers). 
Escolhemos o prefixo do grupo que escutamos através da opção group_prefix.
Com o phyint dizemos que interfaces queremos ativas para o pim. (Não é necessário explicitar , à partida)


   
Ficheiro de configuração router RP

	log all;  
	reverselookup no;  
	phyint eth0 enable;  
	phyint eth1 enable;  
	default_phyint_status enable;  
	group_prefix ff0e::/16;  
	cand_rp;  
	cand_bootstrap_router;


Ficheiro de configuração dos outros routers

    log all;  
	reverselookup no;  
	phyint eth0 enable;  
	phyint eth1 enable;  
	default_phyint_status enable;

Os outros routers têm uma configuração simples pois a biblioteca trata do resto tudo. Esta biblioteca tem um bug e então o static_rp não funciona. Além disso , dá para especificar as interfaces do cand_rp e do cand_bootstrap_router options. Assim como , alguns parâmetros que no nosso caso não foram alterados e, por isso, estão com os valores por default.