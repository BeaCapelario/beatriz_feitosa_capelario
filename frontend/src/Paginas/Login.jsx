import estilo from "./Login.module.css";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const schemaLogin = z.object({
  username: z
    .string()
    .trim()
    .min(1, "Informe um nome")
    .max(5, "Máximo de 5 caracteres"),

  password: z
    .string()
    .trim()
    .min(1, "Informe uma senha")
    .max(3, "Máximo de 3 caracteres"),
});

export function Login() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schemaLogin),
  });

  function enviarDados(data) {
    console.log("Login feito:", data);
    navigate("/inicial");
  }

  return (
    <main>
    <section className={estilo.container}>
      <form className={estilo.formulario} onSubmit={handleSubmit(enviarDados)}>
        <h2 className={estilo.titulo}>Acesso ao Sistema</h2>

        <label htmlFor="usuario">Usuário:</label>
        <input
          id="usuario"
          type="text"
          placeholder="Digite seu usuário"
          {...register("username")}
        />
        {errors.username && (
          <p className={estilo.erro}>{errors.username.message}</p>
        )}

        <label htmlFor="senha">Senha:</label>
        <input
          id="senha"
          type="password"
          placeholder="Digite sua senha"
          {...register("password")}
        />
        {errors.password && (
          <p className={estilo.erro}>{errors.password.message}</p>
        )}

        <button className={estilo.botao}>Entrar</button>
      </form>
    </section>
  </main>
  );
}