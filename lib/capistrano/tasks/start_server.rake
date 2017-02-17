namespace :deploy do
  task 'pip_install' do
    on roles(:all) do
      execute "#{fetch(:pyenv_shims)}/pip3 install -r #{current_path}/requirements.txt"
    end
    
  end
  task 'server_start' do
    on roles(:all) do
      execute "service gpk_intertwine restart"
    end
  end
end
